from tkinter import Toplevel, Label, Frame, Button, X, TOP, BOTTOM, RIGHT, LEFT, NO, YES
from .scrolledList import GenScrolledList, SelectMode
from enum import Enum



class TopLevelScrolledList(Toplevel):
    """ A scrollable list of options a user can select. """

    def __init__(self, parent=None, selectmode=SelectMode.SINGLE, grandparent=None):
        """
            Args:
                parent: The window envoking this frame
                selectmode = Flag to set whether a user can make single or multiple selections
                grandparent = The parent of the window envoking this frame

        """
        Toplevel.__init__(self, parent)
        self.selectmode = selectmode
        self.function = None
        self.selection = None
        self.grandparent = grandparent
        self.__caption = ""
        self.__options = []

    def callback(self, function):
        """ The function to be called when a selection is made """
        self.function = function

    def windowTitle(self, title):
        """ Sets the windows's title """
        self.title = title

    @property
    def caption(self):
        return self.__caption

    @caption.setter
    def caption(self, caption):
        """ Sets the TLSL's caption """
        self.__caption = caption

    @property
    def options(self):
        return self.__options

    @options.setter
    def options(self, options):
        """ Sets the options to display """
        self.__options = options

    def makeSelection(self, selection):
        self.selection = selection
        if self.grandparent != None and self.selectmode == SelectMode.SINGLE:
            self.grandparent.destroy()
        self.function()
        self.destroy()

    def createTPSL(self):
        label = Label(self, text=self.caption)
        label.config(font=('times', 10, 'bold'), width=50)
        label.pack(side=TOP, fill=X, expand=NO)

        slWidget = GenScrolledList(self.options, self, self.selectmode)

        buttonFrame = Frame(self)
        buttonFrame.pack(side=BOTTOM, fill=X, expand=NO)
        Button(buttonFrame, text="Select", command=lambda: self.makeSelection(slWidget.picks)).pack(side=LEFT, expand=YES, fill=X)
        Button(buttonFrame, text="Cancel", command=self.destroy).pack(side=RIGHT, expand=YES, fill=X)


if __name__ == '__main__':
    from tkinter import Tk
    root = Tk()

    def exampleCallback():
        print('Clicked')

    def createSingleChoiceTLSL():
        example = TopLevelScrolledList()
        example.windowTitle('Unit Test Title')
        example.caption = 'Pick one of these options:'
        example.options = ['cat', 'bat', 'rat', 'hat']
        example.callback(exampleCallback)
        example.createTPSL()

    def createMultipleChoiceTLSL():
        example = TopLevelScrolledList()
        example.selectmode = SelectMode.MULTIPLE
        example.windowTitle('Unit Test Title')
        example.caption = 'Pick one of these options:'
        example.options = ['cat', 'bat', 'rat', 'hat']
        example.callback(exampleCallback)
        example.createTPSL()

    Button(root, text="Create Scolled List (single)", command=createSingleChoiceTLSL).pack()
    Button(root, text="Create Scolled List (multiple)", command=createMultipleChoiceTLSL).pack()
    root.mainloop()
    #example.pack()
