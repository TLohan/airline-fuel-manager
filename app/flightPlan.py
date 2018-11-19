from .aircraftService import AircraftService
from .airportService import AirportService
from .airport import Airport, BaseAirport, DestinationAirport
from .aircraft import Aircraft, SelectedAircraft
import itertools

class FlightPlan:

    """
    Attributes:
        aircraft (Aircraft):  the aircraft being used.
        base (BaseAirport): the base airport.
        destinations ([DestinationAirport]): a list of the destination airports.
        fuelBudget (float): the total money spent on the route.
        route ([Leg]): the shortest route. A list of Leg objects.
        totalLength (float): The total length of all the legs.
        totalFuelNeeded (float): The total length of the route.
    """

    def __init__(self, aircraft, base, destinations):
        """
        Args:
            aircraft (Aircraft):  the aircraft being used.
            base (BaseAirport): the base airport.
            destinations ([DestinationAirport]): a list of the destination airports.
        """
        self.aircraft = aircraft
        self.base = base
        self.destinations = destinations # list
        self.fuelBudget = 0
        self.route, self.totalLength = self._findShortestPath() #list, int
        self.setLegs()
        self.totalFuelNeeded = self.aircraft.fuel_efficiency * self.totalLength


    def __str__(self):
        string = "Shortest Route\n"
        for leg in self.route:
            string += "{} to {}: \t {:,d}km\n".format(leg.origin.name, leg.dest.name, int(leg.distance))
        string += "\nTotal length: \t {:,d}km".format(self.totalLength)
        string += "\n\n"
        string += "\n\nFuel needed: {} lt".format(self.totalFuelNeeded)
        return string


    def _findShortestPath(self):
        """ Calculates the shortest possible route between the airports """
        routes = self._routePermutations(self.destinations)
        routeDict = {}
        for route in routes:
            key = route[0].distanceTo(self.base) + route[-1].distanceTo(self.base)
            for ind in range(len(self.destinations)-1):
                key += route[ind].distanceTo(route[ind+1])
            routeDict[int(key)] = route
        distances = list(routeDict.keys())
        distances.sort()
        shortestRoute = [self.base] + routeDict[distances[0]] + [self.base]
        return shortestRoute, distances[0]

    def _routePermutations(self, destinations):
        """ Returns a list of all the possible combinations of the airports provided """
        if len(destinations) == 0: # if there are no destination airports
            return []
        if len(destinations) == 1: #if there is only one destination airport
            return [destinations]
        routes = map(list, itertools.permutations(destinations))
        return routes

    def setLegs(self):
        """ Sets the route into a list of Leg objects """
        result = []
        for ind in range(len(self.route) - 1):
            result.append(Leg(ind, self.aircraft, self.route[ind], self.route[ind + 1]))
        self.route = result

    def checkPlaneRange(self):
        """ Checks to see if the plane has the range to fly each Leg of the route."""
        for leg in self.route:
            if not leg.checkRange():
                raise ValueError ("Plane does not have the range ({}km) to fly the leg from {} to {} ({})km".format(self.aircraft.safe_range, leg.origin.name, leg.dest.name, leg.distance))


    def rankAirportsByValue(self):
        """ Returns ordered lists of the airports by value and by order """
        destinations = [self.base] + self.destinations
        rankByValue = [] + destinations
        rankByOrder = [] + destinations
        rankByValue  = sorted(destinations, key=lambda airport: airport.fuel_cost)
        rankByOrder = sorted(destinations, key=lambda airport: airport.order)
        return rankByValue, rankByOrder


    def generateFuelPlan(self):
        """ Caculates how much fuel should be purchased at each stage of the route """
        airportsByValue, airportsByOrder = self.rankAirportsByValue()
        for leg in self.route:
            leg.fuel_guage_on_arrival = self.aircraft.fuel_guage
            valueRank = airportsByValue.index(leg.origin)
            downStreamCheaperAirports = []
            for airport in airportsByValue[:valueRank]:
                if airport.order > leg.origin.order:
                    downStreamCheaperAirports.append(airport)
            if len(downStreamCheaperAirports) == 0:
                max_refill = self.aircraft.safe_range - self.aircraft.getAbsSafeRange()
                fuelBought, spendHere = self.buyFuel(max_refill, leg.cost_here)
                leg.setMoneySpentHere(spendHere, self.fuelBudget)
                self.fuelBudget += spendHere
                leg.setFuelBoughtHere(fuelBought)
            else:
                downstreamAirports = airportsByOrder[leg.dest.order:]
                count = 0
                for airport in downstreamAirports:
                    count += 1
                    if airport.fuel_cost < leg.origin.fuel_cost:
                        distToCheaperAirport = 0
                        for sub_leg in self.route[leg.origin.order:airport.order]:
                            distToCheaperAirport += sub_leg.distance
                        if self.aircraft.hasRange(distToCheaperAirport):
                            if self.aircraft.getAbsSafeRange() < distToCheaperAirport:
                                fuelBought, spendHere = self.buyFuel(abs(distToCheaperAirport - (self.aircraft.getAbsSafeRange())), leg.cost_here)
                                leg.setMoneySpentHere(spendHere, self.fuelBudget)
                                self.fuelBudget += spendHere
                                leg.setFuelBoughtHere(fuelBought)

                            break
                    else:
                        if count == len(downstreamAirports):
                            max_refill = self.aircraft.safe_range - self.aircraft.getAbsSafeRange()
                            fuelBought, spendHere = self.buyFuel(max_refill, leg.cost_here)
                            leg.setMoneySpentHere(spendHere, self.fuelBudget)
                            self.fuelBudget += spendHere
                            leg.setFuelBoughtHere(fuelBought)
            leg.fuel_guage_on_departure = self.aircraft.fuel_guage
            self.aircraft.fly(leg.distance)



    def buyFuel(self, distance, price):
        """ Purchases the fuel to fly distance at price """
        fuelBought = self.aircraft.buy(distance)
        spendHere = fuelBought * price
        return fuelBought, spendHere

class Leg:
    """
    Models the journey between two airports.

    Attributes:
        order (str): where this leg comes in the overall route
        aircraft (Aircraft): the Aircraft being used
        origin (Airport): the start point for this leg
        dest (Airport): the end point for this leg
        distance (float): the distance between the origin and destination airports
        fuel_required (float): the volume of fuel needed for this leg
        fuel_bought_here (float): the litres of fuel bought here
        money_spent_here (float): the money spent here
        money_spent_so_far (float): the total money spent so far
        fuel_guage_on_arrival (float): the fuel guage when the plane landed here
        fuel_guage_on_departure (float): the fuel gauge when the plane departed on this leg
        cost_here (float): the cost of fuel at the origin airport
    """

    def __init__(self, order, aircraft, origin, dest):
        """
        Args:
            order (str): where this leg comes in the overall route
            aircraft (Aircraft): the Aircraft being used
            origin (Airport): the start point for this leg
            dest (Airport): the end point for this leg
        """
        self.order = order
        self.aircraft = aircraft
        self.origin = origin
        self.dest = dest
        self.fuel_bought_here = 0
        self.money_spent_here = 0
        self.money_spent_so_far = 0
        self.fuel_guage_on_arrival = 0
        self.fuel_guage_on_departure = 0
        self.setOrder(self.order)
        self.__calcDistance()
        self.calcFuelRequired()
        self.cost_here = self.origin.fuel_cost


    def __calcDistance(self):
        """ sets the distance between the origin and destination airports """
        self.distance = self.origin.distanceTo(self.dest)

    def setMoneySpentHere(self, money, spent_so_far):
        """ sets the money_spent_here attribute """
        self.money_spent_here = money
        self.money_spent_so_far = spent_so_far + money

    def setFuelBoughtHere(self, volume):
        """ set sthe fuel bought here attribute """
        self.fuel_bought_here = volume

    def setOrder(self, num):
        """ sets the order attribute """
        if type(self.dest) != BaseAirport:
            self.dest.setOrder(num + 1)

    def calcFuelRequired(self):
        """ sets the fuel required attribute """
        self.fuel_required = self.distance * self.aircraft.fuel_efficiency

    def checkRange(self):
        """ returns True if the plane has the range to fly this leg """
        return self.aircraft.hasRange(self.distance)

if __name__ == "__main__":
    # test code
    import unittest

    class TestFlightPlan(unittest.TestCase):
        def setUp(self):
            aircrafts = AircraftService()
            aircraft = aircrafts.getAircraft('737')
            print(aircraft.code)
            aircraft = SelectedAircraft(aircraft.code, aircraft.code, aircraft.units, aircraft.manufacturer, aircraft.max_distance)
            aircraft.setFuelGuage(60)
            aircraft.updateFuelEfficiency(15)
            airports = AirportService()
            airport = airports.getAirport('DUB')
            baseAirport = BaseAirport(airport.name, airport.city, airport.country, airport.iata, airport.icao, airport.lat, airport.lon, airport.currency)
            print(baseAirport.name)
            destinations = ['JFK','LAX', 'HOU', 'HAV', 'LHR']
            print(destinations)
            destinationAirports = []
            for dest in destinations:
                airport = airports.getAirport(dest)
                destinationAirports.append(DestinationAirport(airport.name, airport.city, airport.country, airport.iata, airport.icao, airport.lat, airport.lon, airport.currency))

            self.fp = FlightPlan(aircraft, baseAirport, destinationAirports)
            self.fp.generateFuelPlan()

        def test_main(self):
            self.assertEqual(100393, int(self.fp.fuelBudget))

        def test_Route(self):
            self.assertEqual('Heathrow', self.fp.route[0].dest.name)

        
        def tearDown(self):
            print("Test Finished")
    unittest.main()
