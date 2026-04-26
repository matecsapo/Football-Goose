# for data handling
from goose.data.goose_data_structures import Games, Standings
from pathlib import Path
from random import randint
import os

# For implementing a forecast
from goose.forecast.forecast import Forecast
from goose.model import Model

# for implementing a template of monte carlo simulations
from abc import ABC, abstractmethod

# Abstract class for performing a monte-carlo simulation forecast for a set of games
    # Each unique competition requires a unique conrete subclass of Monte_Carlo_Simulation to account
    # for differences in competition structure / placement significances
        # these specifications are defined via run_simulation() interpret()
class Monte_Carlo_Simulation(Forecast, ABC):
    # Initialized as a forecast with parameter num_simulations
    def __init__(self, forecast_name, model : Model, games : Games, num_simulations, existing_standings : Standings = None):
        super().__init__(forecast_name, model, games, existing_standings)
        self.num_simulations = num_simulations
        # Monte carlo forecast consists of (list of all simulations , interpretation of simulation)
        # for storing all simulations
        self.simulations : list[Standings] = []
        # for storing interpretation of monte carlo simulation
        self.interpretation = None

    # runs monte carlo simulation forecast according to parameters
    def Run_Forecast(self):
        # run all simulations
        for sim in range(self.num_simulations):
            # run a simulation
            self.run_simulation()
        # retrieve interpretation according to specific competition being monte-carlo-simulated
        self.interpret()
        # store forecast
        self.forecast = (self.interpretation, self.simulations)

    # Executes a simulation of the specificed games
        # appends simulation to self.simulations
    # Requires a concrete competition-specific implementation
    @abstractmethod
    def run_simulation(self):
        pass
    
    # Interprets monte carlo simulation according to specific competition
        # stores interpretation into self.interpretation
    # Requires a concrete competition-specific definition of interpretation
        # ex. prob of winning league, prob of relegation, prob of making semis, etc...
    @abstractmethod
    def interpret(self):
        pass

    # displays forecast to terminal:
        # displays an random example simulation
        # displays the simulation interpretation
    def View_Forecast(self):
        # random example simulation
        print("Random Example Simulation")
        self.simulations[randint(0, self.num_simulations - 1)].view()
        # simulation interpretation
        print("")
        print("Simulation Interpretation")
        print(self.interpretation)

    # saves forecast to folder directory/self.forecast
        # saves random example simulation
        # saves the simulation interpretation
    def Save_Forecast(self, directory : str):
        folder = Path(directory) / self.forecast_name
        os.makedirs(folder, exist_ok=True)
        # random example simulation
        self.simulations[randint(0, self.num_simulations - 1)].save(folder / "example_simulation.csv")
        # simulation interpretation
        self.interpretation.to_csv(folder / "monte-carlo-results.csv")
