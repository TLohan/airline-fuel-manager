"""

aircraftFleet.py

"""
from csv import DictReader
from .aircraft import Aircraft

class AircraftService:
    _aircrafts = {} # class attribute for storing Aircraft objects

    def __init__(self, csv_file_loc="../csvData/aircraft.csv"):
        self.__parseAircraft(csv_file_loc)

    def __parseAircraft(self, csv_file_loc):
        """ parses csv data into Aircraft objects """
        try:
            with open(csv_file_loc, encoding="utf-8") as csvfile:
                readlines = DictReader(csvfile, ["code", "category", "units", "manufacturer", "max_distance"])
                for row in readlines:
                    self._aircrafts[row['code']] = Aircraft(row['code'], row['category'], row['units'], row['manufacturer'], row['max_distance'])
        except IOError:
            raise IOError ("Error! {} is not a valid file".format(csv_file_loc))

    def getAircraft(self, code):
        """ returns an Aircraft object from the class dictionary attribute """
        try:
            aircraft = self._aircrafts[code]
            return aircraft
        except KeyError:
            print("{} not included in csv file supplied!".format(code))

    def getAircraftCodes(self):
        """ return a list of all the Aircraft codes"""
        codes = list(self._aircrafts.keys())
        return codes

if __name__ == '__main__':
    # test code
    import unittest

    class AircraftServiceTest(unittest.TestCase):

        def setUp(self):
            self.inventory = AircraftService()
        
        def test_getAircraft(self):
            aircraft = self.inventory.getAircraft('747')
            self.assertIsInstance(aircraft, Aircraft)

        def test_getAircraftCodes(self):
            codes = self.inventory.getAircraftCodes()
            self.assertTrue(len(codes) > 0)

    unittest.main()
