import tkinter as tk

class FlightPlanFrame:

    def __init__(self, flightPlan, parent):
        self.__COLUMNS = ["LEG", "FROM", "TO", "FUEL_GAUGE", "DISTANCE", 
            "FUEL BOUGHT", "PRICE", "FUEL GAUGE", "€ SPENT", "TOTAL € SPENT"]
        self.flightPlan = flightPlan
        self.flightPlan.generateFuelPlan()
        self.frame = tk.Frame(parent)
        self.frame.grid_rowconfigure(0)
        
    
    def __generateColumns(self):
        for index, column in enumerate(self.__COLUMNS):
            self.frame.grid_columnconfigure(index, weight=1)
            tk.Label(self.frame, text=column, font=("Helvetica", 10), relief=tk.GROOVE).grid(row=1, column=index, sticky="SNEW")

    def __populateGrid(self):
        for ind, leg in enumerate(self.flightPlan.route):
            tk.Label(self.frame, text="{}".format(ind+1)).grid(row=(ind+2), column=0)
            tk.Label(self.frame, text="{}".format(leg.origin.name)).grid(row=(ind+2), column=1)
            tk.Label(self.frame, text="{}".format(leg.dest.name)).grid(row=(ind+2), column=2)
            tk.Label(self.frame, text="{:,d} km ({}%)".format(int(leg.distance), round(self.flightPlan.aircraft.calcPercentOfTank(leg.distance), 0))).grid(row=(ind+2), column=3)
            tk.Label(self.frame, text="{}%".format(round(leg.fuel_guage_on_arrival, 0))).grid(row=(ind+2), column=4)
            tk.Label(self.frame, text="{:,d} lt".format(int(leg.fuel_bought_here))).grid(row=(ind+2), column=5)
            tk.Label(self.frame, text="€{}".format(leg.cost_here)).grid(row=(ind+2), column=6)
            tk.Label(self.frame, text="{}%".format(round(leg.fuel_guage_on_departure, 0))).grid(row=(ind+2), column=7)
            tk.Label(self.frame, text="€{:,d}".format(int(leg.money_spent_here))).grid(row=(ind+2), column=8)
            tk.Label(self.frame, text="€{:,d}".format(int(leg.money_spent_so_far))).grid(row=(ind+2), column=9)
        tk.Label(self.frame, text="End").grid(row=(ind+3), column=0)
        tk.Label(self.frame, text=self.flightPlan.base.name).grid(row=(ind+3), column=1)
        tk.Label(self.frame, text="{}%".format(int(self.flightPlan.aircraft.fuel_guage))).grid(row=(ind+3), column=4)
        tk.Label(self.frame, text="€{:,d}".format(int(self.flightPlan.fuelBudget)), font=("times", 10, "bold")).grid(row=(ind+3), column=9)
    
    def run(self):
        caption = tk.Label(self.frame, text="Flight Plan", font=(12), relief=tk.GROOVE)
        caption.grid(row=0, sticky="SNEW", columnspan=10)
        self.__generateColumns()
        self.__populateGrid()
        return self.frame