from abc import ABC, abstractmethod

# for data storage
from goose.engine.data import Game

# Abstract class defining operations required to be provided by all models
class Model(ABC):

    # Predict specified game according to model
    @abstractmethod
    def Predict_Game(self, game : Game):
        pass

    # Simulate specified game according to model
    @abstractmethod
    def Simulate_Game(self, game : Game):
        pass
