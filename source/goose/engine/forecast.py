from abc import ABC, abstractmethod

# for storing data
from goose.engine.data import Games, Standings_Data

# for employing models
from goose.engine.model import Model

# Abstract class templating Forecast object that define a scheme by which to predict/expect/simulate a given competition 
    # forecast depends on model to use + (optionally) existing/current standings (to combine prediction with)
class Forecast(ABC):
    #  Initialized according to model and set of games to predict
        # Can also supply existing standings to combine predictions with
    def __init__(self, model : Model, games : Games, existing_standings : Standings_Data = None):
        self.model = model
        self.games = games
        self.existing_standings = existing_standings
        # for storing predicted results produced by model
        self.predicted_results = None
        # for storing ultimate combined existied_standings and predicted_results
        self.predicted_standings = None
    
    # Performs full forecast:
        # Precicts out set of games
        # Computes final standings combination of existing_standings and predicted results
    # (Abstract)
    @abstractmethod
    def Forecast(self):
        pass

    # Display predicted results:
        # To temp file
        # To terminal
    # (Abstract)
    @abstractmethod
    def View_Predicted_Results(self):
        pass

    # Display predicted standings:
        # To temp file
        # To terminal
    # (Abstract)
    @abstractmethod
    def View_Predicted_Standings(self):
        pass
        