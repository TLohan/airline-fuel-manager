from tkinter import *
class DestFrame(Frame):
    """ Frame which displays a Destination Airport """
    
    def __init__(self, airport, parent=None):
        Frame.__init__(self, parent)
        self.airport = airport
        self.__make_widgets()
        self.isPacked = False


    def __make_widgets(self):
        """ Adds the Label and Close Button """
        airport = self.airport
        label = Label(self, text=airport.name)
        label.config(relief=GROOVE)
        label.pack(side=LEFT, fill=X, expand=YES)
        button = Button(self, text='X', command=self.nuke)
        button.pack(side=RIGHT, fill=X, expand=NO)

    def packMe(self):
        """ Adds the frame to the parent frame """
        self.pack(side=TOP, fill=X, expand=NO)
        self.isPacked = True

    def nuke(self):
        """ Deletes the DestFrame object and the selected airport """
        self.pack_forget()
        self.isPacked = False

if __name__ == '__main__':
    from tkinter import Tk
    from airport import Airport
    from currency import Currency
    root = Tk()
    fake_currency = Currency('EUR', 'Euro', 1, 1)
    dummyAirport = Airport('Dublin', 'Dublin', '', '', '', 5, 5, fake_currency)
    dest_frame = DestFrame(dummyAirport)
    dest_frame.packMe()
    root.mainloop()