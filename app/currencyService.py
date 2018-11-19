from  csv import DictReader
from .currency import Currency


class CurrencyService():

    def __init__(self, csv_file_loc="../csvData/currencyrates.csv"):
        self._currencies = {} # class attribute for storing Currency objects
        self.__parseCurrencies(csv_file_loc)

    def __parseCurrencies(self, csv_file_loc):
        """ parses csv data into Currency objects """
        try:
            with open(csv_file_loc, encoding="utf-8") as csvfile:
                readlines = DictReader(csvfile)
                for row in readlines:
                    self._currencies[row['code']] = Currency(row['name'], row['name'], row['buys'], row['sells'])
        except IOError:
            raise IOError ("Error! {} is not a valid file".format(csv_file_loc))


    def getCurrency(self, code):
        """ Returns a Currency object from the class dictionary attribute """
        try:
            currency = self._currencies[code]
            return currency
        except KeyError:
            print("{} not included in csv file supplied!".format(code))

if __name__ == "__main__":
    # test code
    import unittest

    class CurrencyServiceTest(unittest.TestCase):

        def setUp(self):
            self.bdc = CurrencyService()
        
        def test_getCurrency(self):
            euro = self.bdc.getCurrency('EUR')
            self.assertEqual(euro.name, 'Euro')

    unittest.main()
