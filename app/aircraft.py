"""
Airplane class

"""

class Aircraft:
    """
    Basic Aircraft superclass.

    Args:
        code (str): the aircraft's unique code.
        category (str): the aircraft's engine type.
        manufacturer (str): the aircraft's manufacturer.
        fuel_efficiency (int): the litres used per km flown.
        max_distance (int): the absolute range of the aircraft in km.
        safe_range (int): the distance the Aircraft can fly with it's margin_of_safety taken into account in km.
        margin_of_safety (int): the minimum range the Aircraft must be able to fly beyond it's safeRange in km.
        image (str): location of the jpg file of the Aircraft's picture.
        tank_size (int): the fuel capacity of the aircraft in litres.
    """
    def __init__(self, code, category, units, manufacturer, max_distance):
        """
        Args:
            code (str): the aircraft's unique code.
            category (str): the aircraft's engine type.
            units (str): the form of the units for max_distance. metric: km, imperial: mi
            manufacturer (str): the aircraft's manufacturer.
            max_distance (int): the absolute range of the aircraft in km.
        """
        self.code = code
        self.category = category
        self.manufacturer = manufacturer
        self.units = units
        self.__setRange(self.units, int(max_distance))
        self.__setTheoreticalLimits()
        self.setMarginOfSafety() # km
        self.setSafeRange()
        self.image = "images/{}.jpg".format(self.code)

    def __str__(self):
        return "{} {}\nMax Range: {} km \nEngine Type: {}".format(
            self.manufacturer, self.code, self.max_distance, self.category)

    def __setRange(self, units, distance):
        """Sets the max_distance to the correct km value """
        if units == 'imperial':
            self.max_distance = int(distance * 1.60934) # km
        else:
            self.max_distance = distance # km

    def setMarginOfSafety(self, MOS=1000):
        """Sets the margin_of_safety"""
        self.margin_of_safety = MOS # km
        self.setSafeTankSize()

    def __setTheoreticalLimits(self, theoretical_max_fuel_efficiency=10):
        """ Sets fuel_efficiency and TANK_SIZE """
        self.fuel_efficiency = theoretical_max_fuel_efficiency # litre/km
        self.TANK_SIZE = self.max_distance * self.fuel_efficiency # litre


    def setMaxDistance(self):
        self.max_distance = self.TANK_SIZE / self.fuel_efficiency
        self.safe_range = self.max_distance - self.margin_of_safety

    def setSafeTankSize(self):
        self.safe_tank_size = self.TANK_SIZE - (self.margin_of_safety * self.fuel_efficiency)

    def setSafeRange(self):
        """ Sets safe_range """
        self.safe_range = self.max_distance - self.margin_of_safety # km

    def hasRange(self, distance):
        """ returns True if safe_range is within distance """
        return True if distance <= (self.safe_tank_size / self.fuel_efficiency) else False

class SelectedAircraft(Aircraft):
    """
    Subclass of Aircraft.
    """

    def __init__(self, code, category, units, manufacturer, max_distance):
        Aircraft.__init__(self, code, category, units, manufacturer, max_distance)
        self.setFuelGuage()


    @classmethod
    def from_base(class_object, baseObject):
        """ Call as SelectedAircraft.from_base(aircraftObject) """
        return class_object(baseObject.code, baseObject.category, baseObject.units, baseObject.manufacturer, baseObject.max_distance)

    def getAbsSafeRange(self):
        """ Gets the absolute safe range of the plane taking into account
            it's current fuel efficiency and the amount of fuel in it's tank.

            Return:
                The total distance the plane could fly with it's current configurations.
        """
        return (self.safe_tank_size / self.fuel_efficiency * self.fuel_guage) / 100


    def calcPercentOfTank(self, distance):
        """ Calculates what percentage of the tank's capacity is required to fly that distance.

            Args:
                distance: The distance in KM that will be flown.

            Returns:
                The percentage of the tank's capacity that distance represents. 
        """
        fuel = distance * self.fuel_efficiency
        return (fuel / self.safe_tank_size) * 100


    def fly(self, distance):
        """ Removes a certain % of fuel from tank
        
            Args:
                distance: The distance in KM the plane will fly.

            Returns:
                None.
        """
        percent_fuel_used = self.calcPercentOfTank(distance)
        self.setFuelGuage(self.fuel_guage - percent_fuel_used)


    def buy(self, distance):
        """ Buy enough fuel for a certain distance. 
        
            Args:
                distance: The distance in KM fuel is bought to cover.

            Returns:
                Volume of fuel to be purchased in litres.
            
            Raises:
                Exception: If the tank can not hold the volume of fuel to travel this distance.
        """
        if self.checkTankHasCapacity(distance):
            percent_fuel_bought = self.calcPercentOfTank(distance) # refill tank by what %
            self.setFuelGuage(self.fuel_guage + percent_fuel_bought)
            return distance * self.fuel_efficiency # litres of fuel bought
        else:
            raise Exception ("Tank can not hold this much fuel!")


    def checkTankHasCapacity(self, distance):
        """ Checks if the plane has enough fuel to fly a certain distance.

            Args:
                distance: The distance in KM the plane needs to travel.

            Returns:
                boolean representation of whether the tank has enough fuel to cover the distance.
        """
        return self.calcPercentOfTank(distance) + self.fuel_guage <= 100.00001

    def setSafeRange(self):
        """ Sets the total safe distance the plane can travel

            Returns:
                The maximum distance the plane can travel minus the current margin of safety.
        """
        self.safe_range = self.max_distance - self.margin_of_safety

    def setFuelGuage(self, percent=100):
        """ Sets the fuel gauge.

            Args:
                percent: the percent of fuel in the tank.

            Raises:
                Exception: if the 'percent' argument is an invalid percentage. 
        """
        if -0.00001 <= percent <= 100.00001:
            self.fuel_guage = percent
        else:
            raise Exception ("Error! Invalid attempt to set fuel guage.")

    def updateFuelEfficiency(self, new_fuel_efficiency):
        self.fuel_efficiency = new_fuel_efficiency
        self.setMaxDistance()
        self.setSafeTankSize()

    def updateMOS(self, new_mos):
        self.margin_of_safety = new_mos
        self.setSafeRange()
        self.setSafeTankSize()


    

if __name__ == '__main__':
    # test code
    import unittest
    
    class AircraftTest(unittest.TestCase):

        def setUp(self):
            self.plane1 = Aircraft('A319', 'jet', 'metric', 'Airbus', 3750)
            self.plane2 = Aircraft('737', 'jet', 'imperial', 'Boeing', 5600)
            self.sp1 = SelectedAircraft('A319', 'jet', 'metric', 'Airbus', 3750)
            self.sp2 = SelectedAircraft('737', 'jet', 'imperial', 'Boeing', 5600)

        def test_hasRange(self):
            self.assertFalse(self.plane1.hasRange(3000))
            self.assertTrue(self.plane2.hasRange(3000))

        def test_setFuelGuage(self):
            self.sp1.setFuelGuage(60)
            self.assertEqual(60, self.sp1.fuel_guage)

        def test_checkFuelCapacity(self):
            self.sp1.setFuelGuage(60)
            self.assertFalse(self.sp1.checkTankHasCapacity(1000000))
            self.assertTrue(self.sp1.checkTankHasCapacity(1000))

        def test_updateFuelEfficiency(self):
            self.sp2.updateFuelEfficiency(15)
            self.assertEqual(15, self.sp2.fuel_efficiency)

    unittest.main()
