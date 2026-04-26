# for defining a template for forecasts 
from abc import ABC, abstractmethod

# for storing data
from goose.data.goose_data_structures import Games, Standings

# for employing models
from goose.model import Model

# Abstract class templating Forecast object which define a scheme by which to predict/expect/simulate a set of games
    # forecast depends on model to use + (optionally) existing/current standings (to combine predictions with)
class Forecast(ABC):
    #  Initialized according to model and set of games to predict
        # Can also supply existing standings to combine predictions with
    def __init__(self, forecast_name, model : Model, games : Games, existing_standings : Standings = None):
        self.forecast_name = forecast_name
        self.model = model
        self.games = games
        self.existing_standings : Standings = existing_standings
        # for storing produced forecast
        self.forecast = None
    
    # Runs full process of the forecast
        # Forecasts out set of games, according to the forecast's prediction logic/approach
    # Stores prioduced forecast into self.forecast
    @abstractmethod
    def Run_Forecast(self):
        pass

    # displays forecast to terminal
    @abstractmethod
    def View_Forecast(self):
        pass

    # saves forecast to folder directory/self.forecast
    @abstractmethod
    def Save_Forecast(self, directory : str):
        pass
