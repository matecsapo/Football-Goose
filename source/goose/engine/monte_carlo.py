# For employing specified forcast
from goose.engine.forecast import Forecast

from abc import ABC, abstractmethod

# Abstract class for performing a monte-carlo simulation for a given competition, given forecast to use
class Monte_Carlo_Simulation(ABC):
    # Initialized according to forecast + simulation parameters
    def __init__(self, forecast : Forecast, num_simulations):
        self.forecast = forecast
        self.num_simulation = num_simulations
        # for storing all predicted_standings simulated by forecast
        self.simulations = []
        # for storing interpretation of monte carlo simulation
        self.interpretation = None

    # runs monte carlo simulation according to forecast and parameters
    def run_simulation(self):
        # run all simulations
        for sim in range(self.num_simulation):
            # run a simulation
            self.forecast.Forecast()
            # store simulation result
            self.simulations.append(self.forecast.predicted_standings)
        # retrieve interpretation according to forecast
        self.interpret()
    
    # Interprets monte carlo simulation according to specific competition
    # (Abstract) --> specified according to specific competition
    @abstractmethod
    def interpret(self):
        pass

    # view interpretation
    # (Abstract)
    @abstractmethod
    def view_interpretation(self):
        pass
