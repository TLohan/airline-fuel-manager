from app.aircraftService import AircraftService
from app.airportService import AirportService
from app.currencyService import CurrencyService
from app.gui import GraphicalUserInterface

def main():
    currencyService = CurrencyService(csv_file_loc="./csvData/currencyrates.csv")
    aircraftService = AircraftService(csv_file_loc="./csvData/aircraft.csv")
    airportService = AirportService(currencyService, country_csv_file_loc="./csvData/countrycurrency.csv", airport_csv_file_loc="./csvData/airport.csv")
    gui = GraphicalUserInterface(aircraftService=aircraftService, airportService=airportService)
    gui.run()


if __name__ == '__main__':
    main()