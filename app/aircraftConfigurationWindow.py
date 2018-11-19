import tkinter as tk
from PIL import ImageTk as imgtk
from PIL import Image

class AircraftConfigurationWindow:

    def __init__(self, selectedAircraft):
        self.selectedPlane = selectedAircraft
        self.TANK_SIZE = selectedAircraft.TANK_SIZE

    def run(self):
        self.window = tk.Toplevel()
        tk.Label(self.window, text="{} {}".format(self.selectedPlane.manufacturer, self.selectedPlane.code), font=('Verdana', 15)).pack(side=tk.TOP) # Title For window
        
        image = self.__getImage()
        if image != None: image.pack(fill=tk.BOTH)
        
        self.__generateFrames()
        self.__initialiseVariables()
        self.__setVariables()
        self.__populateFrames()

    
    def __generateFrames(self):
        self.mainFrame = tk.Frame(self.window) # This frame will hold all the attributes. Split left and right for display.
        self.leftFrame = tk.Frame(self.mainFrame)
        self.leftFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
        self.rightFrame = tk.Frame(self.mainFrame)
        self.rightFrame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=tk.YES)

    def __initialiseVariables(self):
        self.fuelEff_var = tk.IntVar()
        self.MOS_var = tk.IntVar()
        self.maxDist_var = tk.IntVar()
        self.safeRange_var = tk.IntVar()
        self.fuelGuage_var = tk.IntVar()
        self.safeTankSize_var = tk.IntVar()
        self.max_dist_str = tk.StringVar()
        self.safeRange_str = tk.StringVar()



    def __setVariables(self):
        self.fuelEff_var.set(self.selectedPlane.fuel_efficiency)
        self.MOS_var.set(self.selectedPlane.margin_of_safety)
        self.maxDist_var.set(self.selectedPlane.max_distance)
        self.safeRange_var.set(self.selectedPlane.safe_range)
        self.fuelGuage_var.set(self.selectedPlane.fuel_guage)
        self.safeTankSize_var.set(self.selectedPlane.safe_tank_size)
        self.max_dist_str.set("Max Range: {:,d} km".format(int(self.selectedPlane.max_distance)))
        self.safeRange_str.set("Safe Range: {:,d} km".format(int(self.selectedPlane.safe_range)))

    def FuelEffonMove(self, value):
        self.fuelEff_var.set(value)
        maxD = self.TANK_SIZE/int(value)
        self.maxDist_var.set(maxD)
        self.safeTankSize_var.set(self.TANK_SIZE - (self.MOS_var.get() * int(value)))
        sr = (maxD - self.MOS_var.get()) * self.fuelGuage_var.get() / 100
        self.safeRange_var.set(sr)
        self.max_dist_str.set("Max Range: {:,d} km".format(int(maxD)))
        self.safeRange_str.set("Safe Range: {:,d} km".format(int(sr)))


    def MOSonMove(self, value):
        self.MOS_var.set(value)
        sr = (self.maxDist_var.get() - int(value)) * self.fuelGuage_var.get() / 100
        self.safeRange_var.set(sr)
        self.safeTankSize_var.set(self.TANK_SIZE - (self.fuelEff_var.get() * int(value)))
        self.safeRange_str.set("Safe Range: {:,d} km".format(int(sr)))

    def FuelGuageonMove(self, value):
        self.fuelGuage_var.set(value)
        sr = (self.maxDist_var.get() - self.MOS_var.get())
        self.safeRange_var.set(sr)
        sr = (self.maxDist_var.get() - self.MOS_var.get()) * self.fuelGuage_var.get() / 100
        self.safeRange_str.set("Safe Range: {:,d} km".format(int(sr)))

    def updatePlane(self):
        self.selectedPlane.max_distance = self.maxDist_var.get()
        self.selectedPlane.fuel_efficiency = self.fuelEff_var.get()
        self.selectedPlane.margin_of_safety = self.MOS_var.get()
        self.selectedPlane.safe_range = self.safeRange_var.get()
        self.selectedPlane.fuel_guage = self.fuelGuage_var.get()
        self.selectedPlane.safe_tank_size = self.safeTankSize_var.get()
        self.window.destroy()

    def __populateFrames(self):
        tk.Label(self.leftFrame, textvariable= self.max_dist_str).pack(side=tk.TOP)
        tk.Label(self.leftFrame, text="Tank Size: {:,d} litres".format(int(self.selectedPlane.TANK_SIZE))).pack(side=tk.TOP)
        tk.Label(self.rightFrame, text="Engine: {}".format(self.selectedPlane.category)).pack(side=tk.TOP)
        tk.Label(self.rightFrame, textvariable= self.safeRange_str ).pack(side=tk.TOP)

        self.mainFrame.config(pady=50)
        self.mainFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

        fuelGuageGroup = tk.LabelFrame(self.leftFrame, text="Tank % Full")
        fuelGuageGroup.pack(side=tk.TOP, padx=10, pady = 10)
        fuelGuageScale = tk.Scale(fuelGuageGroup, from_=0, to=100, orient=tk.HORIZONTAL, variable=self.fuelGuage_var, command= self.FuelGuageonMove) # limit efficiencies from 5 to 30 km/l
        #fuelGuageScale.set(self.fuelGuage) # set default to current Aircraft.fuelGuage value.
        fuelGuageScale.pack(side=tk.LEFT)
        tk.Button(fuelGuageGroup, text="Reset").pack(side=tk.LEFT)

        efficencyGroup = tk.LabelFrame(self.leftFrame, text="Fuel Efficiency (l/km)")
        efficencyGroup.pack(side=tk.TOP, padx=10, pady = 10)
        fuelEfficiencyScale = tk.Scale(efficencyGroup, from_=10, to=30, orient=tk.HORIZONTAL, variable=self.fuelEff_var, command= self.FuelEffonMove) # limit efficiencies from 5 to 30 km/l
        fuelEfficiencyScale.set(self.selectedPlane.fuel_efficiency) # set default to current Aircraft.fuelEfficiency value.
        fuelEfficiencyScale.pack(side=tk.LEFT)
        tk.Button(efficencyGroup, text="Reset", command=lambda: self.selectedPlane.updateFuelEfficiency(fuelEfficiencyScale.get())).pack(side=tk.LEFT) #self.updateFuelEfficiency(fuelEfficiencyScale.get())

        MOSGroup = tk.LabelFrame(self.rightFrame, text="Margin of Safety (km)")
        MOSGroup.pack(side=tk.TOP, padx=10, pady = 10)
        MOSScale = tk.Scale(MOSGroup, from_=500, to=1500, orient=tk.HORIZONTAL, variable=self.MOS_var, command=self.MOSonMove) # limit mos from 500 to 3000 km
        MOSScale.set(self.selectedPlane.margin_of_safety) # set default to current Aircraft.margin_of_safety value.
        MOSScale.pack(side=tk.LEFT)
        tk.Button(MOSGroup, text="Reset", command=lambda: self.selectedPlane.updateMOS(MOSScale.get())).pack(side=tk.LEFT)
        buttonFrame = tk.Frame(self.window)
        tk.Button(buttonFrame, text='Confirm', command=self.updatePlane).pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)
        tk.Button(buttonFrame, text='Cancel', command= self.window.destroy).pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)
        buttonFrame.pack(side=tk.BOTTOM, fill=tk.X, expand=tk.NO)

    def __getImage(self):
        try:
            maxsize = (240, 240)
            im = Image.open(self.selectedPlane.image) # opens the Aircraft.image to be passed PIL.ImageTk.PhotoImage, need this for jpg
            im.thumbnail(maxsize, Image.ANTIALIAS) # SCALE the image, not crop it
            tkim = imgtk.PhotoImage(image = im)
            pic = tk.Label(self.window, image=tkim)
            pic.image  = tkim # VERY IMPORTANT!! wont display picture otherwise
            return pic
        except FileNotFoundError:
            return None

if __name__ == '__main__':
    from aircraft import Aircraft, SelectedAircraft
    aircraft = SelectedAircraft.from_base(Aircraft('A319', 'jet', 'metric', 'Airbus', 3750))
    AircraftConfigurationWindow(aircraft)