from tkinter import *
from enum import Enum

class SelectMode(Enum):
    SINGLE = 1,
    MULTIPLE = 2

class GenScrolledList(Frame):
    def __init__(self, options, parent=None, selectmode = SelectMode.SINGLE):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)
        self.__selectmode = selectmode
        self.makeWidgets(options)
        self.selected = []
        self.picks = []
        self.poll()

    def poll(self):
        now = self.listbox.curselection()
        if now != self.selected:
            self.selected = now
            if len(self.selected):
                self.list_has_changed(now)
        self.after(250, self.poll)

    def list_has_changed(self, selection):
        if self.__selectmode == SelectMode.SINGLE:
            self.picks = [self.listbox.get(selection[0])]
        elif self.__selectmode == SelectMode.MULTIPLE:
            self.picks = []
            for index in selection:
                self.picks += [self.listbox.get(index)]

    def makeWidgets(self, options):
        sbar = Scrollbar(self)
        if self.__selectmode == SelectMode.SINGLE:
            list = Listbox(self, relief=SUNKEN, selectmode=SINGLE)
        elif self.__selectmode == SelectMode.MULTIPLE:
            list = Listbox(self, relief=SUNKEN, selectmode=MULTIPLE)
        else:
            print('ERROR!: invalid selectmode entered. s (single) or m (multiple)')
        sbar.config(command=list.yview)
        list.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        list.pack(side=LEFT, expand=YES, fill=BOTH)
        pos = 0
        for label in options:
            list.insert(pos, label)
            pos += 1
        self.listbox = list
