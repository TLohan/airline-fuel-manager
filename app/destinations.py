from .destinationFrame import DestFrame
from tkinter import Frame, Label, Button, GROOVE, LEFT, X, YES, NO, RIGHT

class Destinations:
    """ The list of destination airports """

    def __init__(self):
        self.__airports = []
        self.__destinationFrames = []

    @property
    def airports(self):
        return self.__airports

    def addAirport(self, airport):
        """ Adds an airport to the list of desitinations """
        if airport not in self.__airports:
            self.__airports.append(airport)
    
    def removeAirport(self, airport):
        """ Removes an airport from the list of destinations """
        self.__airports.remove(airport)

    @property
    def destinationFrames(self):
        return self.__destinationFrames

    def generateDestinationFrames(self, parent):
        for airport in self.airports:
            self.addDestinationFrame(airport, parent)


    def addDestinationFrame(self, airport, parent=None):
        destinationFrame = Frame(parent)
        label = Label(destinationFrame, text=airport.name)
        label.config(relief=GROOVE)
        label.pack(side=LEFT, fill=X, expand=YES)
        button = Button(destinationFrame, text='X', command=lambda: self.removeDestinationFrame(airport, destinationFrame))
        button.pack(side=RIGHT, fill=X, expand=NO)
        self.__destinationFrames.append(destinationFrame)
    
    def removeDestinationFrame(self, airport, destinationFrame):
        destinationFrame.pack_forget()
        self.__destinationFrames.remove(destinationFrame)
        self.removeAirport(airport)