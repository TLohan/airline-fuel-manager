from csv import DictReader
from .currencyService import CurrencyService
from .airport import Airport


class AirportService:
    _airport_dict = {} # iata code: Airport object
    _country_dict = {} # country name: list of Airport objects
    _airports_byName_dict = {} # airport name: Airport object
    _airports_byAlpha_dict = {} # letter of alphabet: Airport object's whose name begins with that letter
    _airports_byCountry_dict = {} 

    def __init__(self, currencyService, country_csv_file_loc="../csvData/countrycurrency.csv", airport_csv_file_loc="../csvData/airport.csv"):
        self.currencyService = currencyService
        self.__setAirportsByAlphaDict()
        self.__parseCountries(country_csv_file_loc)
        self.__parseAirports(airport_csv_file_loc)

    def __parseAirports(self, csv_file_loc):
        """ parses csv data into Airport objects """
        try:
            with open(csv_file_loc, encoding="utf-8") as csvfile:
                linereader = DictReader(csvfile, ['num', 'name', 'city', 'country', 'iata', 'icao', 'lat', 'lon'])
                for row in linereader:
                    currency_code = self.getCountryCurrency(row['country'].lower())
                    currency = self.currencyService.getCurrency(currency_code)
                    if currency != None:
                        airport = Airport(row['name'], row['city'].title(), row['country'].title(), row['iata'], row['icao'], row['lat'], row['lon'], currency)
                        self._airport_dict[airport.iata] = airport
                        self._airports_byName_dict[airport.name] = airport
                        
                        try:
                            self._airports_byCountry_dict[row['country']].append(airport)
                        except KeyError:
                            self._airports_byCountry_dict[row['country']] = [airport]
                       
                        try:
                            self._airports_byAlpha_dict[airport.name[0].upper()].append(airport)
                        except KeyError:
                            self._airports_byAlpha_dict['misc'].append(airport)
                            try:
                                self._airports_byCountry_dict[airport.country].append(airport)
                            except KeyError:
                                self._airports_byCountry_dict['misc'].append(airport)

                csvfile.close()
        except FileNotFoundError as e:
            print(e)


    def __parseCountries(self, csv_file_loc):
        """ parses csv data into Currency objects """
        try:
            with open(csv_file_loc, encoding="utf-8") as csvfile:
                linereader = DictReader(csvfile)
                for row in linereader:
                    if row['currency_alphabetic_code'] != "":
                        self._country_dict[row['name'].lower()] = row['currency_alphabetic_code']
                csvfile.close()
        except FileNotFoundError as e:
            print(e)

    def __setAirportsByAlphaDict(self):
        """ populates the _airports_byAlpha_dict with key = letter, value = list of airports starting with that letter """
        for char in range(65, 91):
            self._airports_byAlpha_dict[chr(char)] = []
        self._airports_byAlpha_dict['misc'] = []

    def getLetters(self):
        """ returns a list of letters """
        return list(self._airports_byAlpha_dict.keys()) # list

    def getAirportsByLetter(self, letter):
        """ returns a list of the airports starting with letter """
        airports = [airport.name for airport in self._airports_byAlpha_dict[letter]]
        airports.sort()
        return airports # list

    def getCountryNames(self):
        """ returns a list of the names of the countries """
        countries = [country.title() for country in self._airports_byCountry_dict.keys()]
        #countries = list(self._airports_byCountry_dict.keys())
        countries.sort()
        return countries #list

    def getAirportCodes(self):
        """ returns a list all the airport iata codes """
        codes = list(self._airport_dict.keys())
        codes.sort()
        return codes # list

    def getAirportsFromCountry(self, country):
        """ returns a list of all the airports from country: name """
        airports = [airport.name.title() for airport in self._airports_byCountry_dict[country]]
        # airportsByCountry = self._airports_byCountry_dict[name]
        # for airport in airportsByCountry:
        #     airports.append(airport.name)
        airports.sort()
        return airports # list

    def findAirportByName(self, name):
        try:
            return self._airports_byName_dict[name]
        except KeyError:
            raise KeyError("{} not found in system's known airports.".format(name))


    def getCountryCurrency(self, name):
        """ returns the currency code for a country """
        try:
            country_currency_code = self._country_dict[name]
            return country_currency_code
        except KeyError:
            print("{} not included in csv file supplied!".format(name))

    def getAirport(self, code):
        """ returns an Airport object from the class dictionary attribute """
        try:
            airport = self._airport_dict[code]
            return airport
        except KeyError:
            raise KeyError("{} not an airport included in that csv file!".format(code))

    def airportExists(self, code):
        """ Returns True if airport exists """
        try:
            self.getAirport(code)
            return True
        except KeyError:
            return False


if __name__ == "__main__":
    # test code
    import unittest

    class AirportServiceTest(unittest.TestCase):

        def setUp(self):
            self.airportAtlas = AirportService()

        def test_findAirportByName(self):
           name = 'Dublin'
           result = self.airportAtlas.findAirportByName(name).name
           self.assertEqual(name, result)
        
        def test_getAirportsByLetter(self):
            airport_names = self.airportAtlas.getAirportsByLetter('A')
            self.assertTrue(len(airport_names) > 0)
            for name in airport_names:
                self.assertEqual(name[0], 'A')
    
    unittest.main()
