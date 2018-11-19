"""
Airport.py

"""

import math

class Airport:
    """ Models an Airport

        Args:
            name: The name of the airport
            city: The city of the airport
            country: The country of the airport
            iata: The International Air Transport Association 3 letter code for the airport
            icao: The International Civil Aviation Organisation 4 letter code for the airport
            lat: The latitudinal location of the airport
            lon: The longitudinal location of the airport
            currency: The currency of the country where the airport is located


    """

    def __init__(self, name, city, country, iata, icao, lat, lon, currency):
        self.name = name
        self.city = city
        self.country = country
        self.iata = iata
        self.icao = icao
        self.lat = float(lat)
        self.lon = float(lon)
        self.currency = currency
        self.fuel_cost = self.currency.buys

    def distanceTo(self, other):
        """ Calculates the distance between two airports in km using the Haversine formula 
        
            Args:
                other: the desination airport
            
            Returns:
                float: the distance between the airports
        """
        R = 6371 # kilometres
        lat1, lon1, lat2, lon2 = self.lat, self.lon, other.lat, other.lon
        theta1 = math.radians(lat1)
        theta2 = math.radians(lat2)
        delta_theta = math.radians(abs(lat2 - lat1))
        delta_lambda = math.radians(abs(lon2 - lon1))

        a = math.sin(delta_theta/2) * math.sin(delta_theta/2) + math.cos(theta1) * math.cos(theta2) * math.sin(delta_lambda/2) * math.sin(delta_lambda/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        return R * c

    def __eq__(self, value):
        try:
           return self.iata == value.iata
        except AttributeError:
            return False

class DestinationAirport(Airport):
    """ Models a Destination Airport the Aircraft will visit on the route. """
    _destinationAirports = []

    def __init__(self, name, city, country, iata, icao, lat, lon, currency):
        Airport.__init__(self, name, city, country, iata, icao, lat, lon, currency)

    @classmethod
    def from_base(class_object, baseObject):
        """ Call as DestinationAirport.from_base(airportObject) """
        return class_object(baseObject.name, baseObject.city, baseObject.country, baseObject.iata, baseObject.icao, baseObject.lat, baseObject.lon, baseObject.currency)

    def setOrder(self, num):
        self.order = num




class BaseAirport(Airport):
    """ Models the Base Airport from which the route will be operated from. """
    def __init__(self, name, city, country, iata, icao, lat, lon, currency):
        Airport.__init__(self, name, city, country, iata, icao, lat, lon, currency)
        self.order = 0

    @classmethod
    def from_base(class_object, baseObject):
        """ Call as BaseAirport.from_base(airportObject) """
        return class_object(baseObject.name, baseObject.city, baseObject.country, baseObject.iata, baseObject.icao, baseObject.lat, baseObject.lon, baseObject.currency)

    def __str__(self):
        return "Name: {}\nIATA Code: {}\nCity: {}\nCountry:{}\nCurrency: {}".format(self.name, self.iata, self.city, self.country, self.currency.name)

if __name__ == '__main__':
    #self-test code
    from .currency import Currency
    import unittest

    class AirportTest(unittest.TestCase):

        def setUp(self):
            fake_currency = Currency('EUR', 'Euro', 1, 1)
            self.airport_a = Airport('Herat', 'Herat', 'Afghanistan', 'HEA', 'OAHR', 34.210017, 62.2283, fake_currency)
            self.airport_b = Airport('Es Senia', 'Oran', 'Algeria', 'ORN', 'DAOO', 35.623858, -0.621183, fake_currency)
        
        def test_distanceTo(self):
            distance_from_a_to_b = self.airport_a.distanceTo(self.airport_b)
            distance_from_b_to_a = self.airport_b.distanceTo(self.airport_a)
            self.assertEqual(distance_from_a_to_b, distance_from_b_to_a)
    
    class BaseAirportTest(unittest.TestCase):

        def setUp(self):
            fake_currency = Currency('EUR', 'Euro', 1, 1)
            self.airport = BaseAirport('Herat', 'Herat', 'Afghanistan', 'HEA', 'OAHR', 34.210017, 62.2283, fake_currency)
        
        def test_print(self):
            expected = "Name: Herat\nIATA Code: HEA\nCity: Herat\nCountry:Afghanistan\nCurrency: Euro"
            actual = str(self.airport)
            self.assertEqual(actual, expected)

    unittest.main()


