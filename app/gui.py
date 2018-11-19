import tkinter as tk
from tkinter.messagebox import showerror, showwarning, showinfo
from .topLevelScrolledList import TopLevelScrolledList, SelectMode
from .airportService import AirportService
from .aircraftService import AircraftService
from .aircraft import SelectedAircraft
from .airport import Airport, BaseAirport, DestinationAirport
from .flightPlan import FlightPlan
from .destinationFrame import DestFrame
from .destinations import Destinations
from .aircraftConfigurationWindow import AircraftConfigurationWindow
from .flightPlanFrame import FlightPlanFrame
from PIL import ImageTk as imgtk
from PIL import Image

class GraphicalUserInterface:

    def __init__(self, aircraftService, airportService):
        self.selectedAirports = []
        self.selectedPlane = None # plane object
        self.baseAirport = None # airport object
        self.destinations = Destinations()
        self.aircraftService = aircraftService
        self.airportService = airportService
        self.airportMenuWidget = None
        self.__defineDefaults()
        self.__initialiseFrames()
        
    def __initialiseFrames(self):
        self.shellFrame = None
        self.baseFrame = None
        self.flightPlanFrame = None

    def __defineDefaults(self):
        defaultBaseAirport = self.airportService.getAirport('DUB')
        self.baseAirport = BaseAirport.from_base(defaultBaseAirport)
        defaultAircraft = self.aircraftService.getAircraft('777')
        self.selectedPlane = SelectedAircraft.from_base(defaultAircraft)


    def check_clash(self, picks):
        for pick in picks:
            if type(pick) == type(self.baseAirport) or pick == self.baseAirport.iata:
                errorMsg = 'Error! {} is the base airport!\n Removed from list of destination airports.'.format(pick)
                picks.pop(picks.index(pick))
                tk.messagebox.showerror('Error!', errorMsg)
        return picks

    def pick_plane(self, root):
        planeTLSL = TopLevelScrolledList(root)
        planeTLSL.windowTitle("Select Airplane.")
        planeTLSL.caption = "Select plane from options:"
        planeTLSL.options = self.aircraftService.getAircraftCodes()
        planeTLSL.callback(lambda: self.set_plane(planeTLSL.selection))
        planeTLSL.createTPSL()

    def set_plane(self, code):
        plane = self.aircraftService.getAircraft(code[0])
        self.selectedPlane = SelectedAircraft.from_base(plane)
        self.set_GUI()

    def pick_airports(self, key):
        """Displays three buttons to select airport by CODE, COUNTRY, or NAME"""
        top = tk.Toplevel(self.root)
        self.airportMenuWidget = top if key == 'base' else None
        caption = tk.Label(top, text="How would you like to select the airports?")
        caption.config(font=('times', 10, 'bold'), width=50)
        caption.pack(side=tk.TOP)
        tk.Button(top, text="by country", command=lambda: self.pick_country(key, top)).pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
        tk.Button(top, text="by name", command= lambda: self.airports_by_name(key, top)).pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
        tk.Button(top, text="by code", command=lambda: self.pick_by_iata_code(key, top)).pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
        searchFrame = tk.Frame(top)
        searchFrame.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
        searchFrame.grid_columnconfigure(0, weight=1)
        searchFrame.grid_columnconfigure(1, weight=1)
        searchFrame.grid_columnconfigure(2, weight=1)
        tk.Label(searchFrame, text="Enter code(s):").grid(row=0, column=0, sticky="NSEW")
        searchCode = tk.Entry(searchFrame)
        searchCode.grid(row=0, column=1, sticky="NSEW")
        tk.Button(searchFrame, text="Add", command=lambda: self.search_by_code(searchCode, key)).grid(row=0, column=2, sticky="NSEW")

    def search_by_code(self, entryWidget, key):
        codes = entryWidget.get()
        codes = codes.split(',')
        for ind, code in enumerate(codes):
            codes[ind] = code.upper().strip()
            entryWidget.delete(0, tk.END)
            if not self.airportService.airportExists(codes[ind]):
                tk.messagebox.showerror("Bad input", "{} not a known airport. Try again.".format(codes[ind]))
                codes.remove(codes[ind])
        self.set_airports(codes, key)

    def pick_country(self, key, parent=None):
        """ Displays list of countries, selected country gets passed to airportByCountry()"""
        TLSL = TopLevelScrolledList(parent)
        TLSL.callback(lambda: self.airport_by_country(TLSL.selection, key, parent))
        TLSL.windowTitle("Select Country")
        TLSL.caption = "Select a country from below:" 
        TLSL.options = self.airportService.getCountryNames()
        TLSL.createTPSL()

    def airport_by_country(self, country, key, parent=None, grandparent=None):
        """Displays a list of countries from a certain country, ammends selection to selectedAirports"""
        country = country[0]
        selectmode = SelectMode.SINGLE if key == 'base' else SelectMode.MULTIPLE
        TLSL = TopLevelScrolledList(parent, selectmode, grandparent)
        TLSL.callback(lambda: self.set_airports_from_name(TLSL.selection, key, TLSL))
        TLSL.windowTitle(country)
        TLSL.caption = "Select an airport from {}".format(country)
        TLSL.options = self.airportService.getAirportsFromCountry(country)
        TLSL.createTPSL()

    def airports_by_name(self, key, parent):
        TLSL = TopLevelScrolledList(parent)
        TLSL.callback(lambda: self.pick_airports_alphabetically(TLSL.selection, key, parent))
        TLSL.caption = "Filter airports by letter:"  
        TLSL.options = self.airportService.getLetters()
        TLSL.createTPSL()

    def pick_airports_alphabetically(self, letter, key, parent=None):
        letter = letter[0]
        selectmode = SelectMode.SINGLE if key == 'base' else SelectMode.MULTIPLE
        TLSL = TopLevelScrolledList(parent, selectmode)
        TLSL.callback(lambda: self.set_airports_from_name(TLSL.selection, key, TLSL))
        TLSL.caption ="Airports beginning with letter: {}".format(letter)
        airportsByLetter = self.airportService.getAirportsByLetter(letter)
        TLSL.options = airportsByLetter 
        TLSL.createTPSL()

    def set_airports_from_name(self, picks, key, windowToKill=None):
        apObjs = []
        for name in picks:
            airport = self.airportService.findAirportByName(name)
            apObjs.append(airport.iata)
        self.set_airports(apObjs, key, windowToKill)

    def pick_by_iata_code(self, key, parent):
        selectmode = SelectMode.SINGLE if key == 'base' else SelectMode.MULTIPLE
        TLSL = TopLevelScrolledList(parent, selectmode)
        TLSL.callback(lambda: self.set_airports(TLSL.selection, key, TLSL))
        TLSL.windowTitle("Select by IATA code.")
        TLSL.caption = "Select from the IATA codes below:"
        iataCodes = self.airportService.getAirportCodes()
        iataCodes.sort()
        TLSL.options = iataCodes 
        TLSL.createTPSL()

    def set_airports(self, picks, key, windowToKill=None):
        if key == "dest":
            for ind in range(len(picks)):
                picks = self.check_clash(picks)
            for ind in range(len(picks)):
                airport = self.airportService.getAirport(picks[ind])
                self.destinations.addAirport(DestinationAirport.from_base(airport))
        else:
            if windowToKill != None:
                self.airportMenuWidget.destroy()
            airport = self.airportService.getAirport(picks[0])
            self.baseAirport = BaseAirport.from_base(airport)
        if windowToKill != None:
            windowToKill.destroy()
        self.set_GUI()

    def set_flight_plan(self, root):
        if self.baseAirport != None and self.destinations.airports != [] and self.selectedPlane != None:
            flightPlan = FlightPlan(self.selectedPlane, self.baseAirport, self.destinations.airports)
            try:
                flightPlan.checkPlaneRange()
                if self.flightPlanFrame != None: self.flightPlanFrame.pack_forget()
                self.flightPlanFrame = self.createFlightPlanFrame(flightPlan, root)
                self.set_GUI()
            except ValueError as err:
                tk.messagebox.showwarning("Plane Range", str(err))
        else:
            tk.messagebox.showwarning("Oops", "Insufficient Information.")


    def set_GUI(self):
        if self.shellFrame != None: self.shellFrame.pack_forget()
        self.shellFrame = tk.Frame(self.root, width=600)
        self.shellFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

        planeFrame = tk.Frame(self.shellFrame, bd=1, relief=tk.GROOVE)
        tk.Button(planeFrame, text="Pick Airplane", command=lambda: self.pick_plane(self.root), width=20).pack(side=tk.TOP, expand=tk.NO, fill=tk.X)
        planeFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

        self.__createBaseFrame()
        self.__populateBaseFrame()
        self.baseFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

        destinationFrame = tk.Frame(self.shellFrame, bd=1, relief=tk.GROOVE)
        tk.Button(destinationFrame, text="Pick Destination Airports", command=lambda: self.pick_airports('dest'), width=35).pack(side=tk.TOP, expand=tk.NO, fill=tk.X)
        destinationFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

        if self.selectedPlane != None:
            self.createConfigureAircraftWidget(planeFrame)
    
        if self.destinations.airports != []:
            self.destinations.generateDestinationFrames(destinationFrame)
            for destinationFrame in self.destinations.destinationFrames:
                destinationFrame.pack(side=tk.TOP, fill=tk.X, expand=tk.NO)
        if self.flightPlanFrame != None:
            self.flightPlanFrame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)

    def __createBaseFrame(self):
        self.baseFrame = tk.Frame(self.shellFrame, bd=1, relief=tk.GROOVE)
        self.baseFrame.grid_rowconfigure(0)
        self.baseFrame.grid_columnconfigure(0, weight=1)
        self.baseFrame.grid_columnconfigure(1, weight=1)
        tk.Button(self.baseFrame, text="Pick Base Airport", command=lambda: self.pick_airports('base'), width=35).grid(row=0, sticky="SNEW", columnspan=2)

    def __populateBaseFrame(self):
        if self.baseAirport != None:
            tk.Label(self.baseFrame, text="Name:").grid(row=1, column=0)
            tk.Label(self.baseFrame, text="IATA:").grid(row=2, column=0)
            tk.Label(self.baseFrame, text="City:").grid(row=3, column=0)
            tk.Label(self.baseFrame, text="Country:").grid(row=4, column=0)
            tk.Label(self.baseFrame, text="Currency:").grid(row=5, column=0)
            tk.Label(self.baseFrame, text=self.baseAirport.name).grid(row=1, column=1, sticky="W")
            tk.Label(self.baseFrame, text=self.baseAirport.iata).grid(row=2, column=1, sticky="W")
            tk.Label(self.baseFrame, text=self.baseAirport.city).grid(row=3, column=1, sticky="W")
            tk.Label(self.baseFrame, text=self.baseAirport.country).grid(row=4, column=1, sticky="W")
            tk.Label(self.baseFrame, text=self.baseAirport.currency.name).grid(row=5, column=1, sticky="W")
        else:
            tk.Label(self.baseFrame, text="Undefined").grid(row=1, column=0)
            
    def run(self):
        self.root = tk.Tk()
        self.root.title('OOP Project')
        tk.Button(self.root, text="Calculate Route", command=lambda: self.set_flight_plan(self.root)).pack(side=tk.BOTTOM, fill=tk.X, expand=tk.NO)
        self.set_GUI()
        self.root.mainloop()

    def createConfigureAircraftWidget(self, parent=None):
        tk.Label(parent, text = "{} {}".format(self.selectedPlane.manufacturer, self.selectedPlane.code)).pack(side=tk.TOP)
        tk.Button(parent, text="Configure", command=lambda: self.createConfigureAircraftWindow()).pack(side=tk.BOTTOM)

    def createConfigureAircraftWindow(self):
        configureAircraftWindow = AircraftConfigurationWindow(self.selectedPlane)
        configureAircraftWindow.run()

    def createDestinationWidget(self, destinationAirport, parent=None):
        return DestFrame(destinationAirport, parent)

    def createFlightPlanFrame(self, flightPlan, parent):
        """ Creates the GUI widget to display a visualisation of the data to the user """
        flightPlanFrame = FlightPlanFrame(flightPlan, parent)
        return flightPlanFrame.run()



