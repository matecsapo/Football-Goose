# for creating a standardized template for goose's native models
from goose.engine.model import Model
from abc import ABC, abstractmethod

# for data handling
import json

# Abstract class Goose_Model to standardize the behaviour of all of goose's native models
# all goose native models (found in package goose.models) are concrete subclasses of Goose_Model
class Goose_Model(Model, ABC):
    # all goose-native models are iniatialized with only argument as model_name for
    # simplicity and uniformity

    # all goose-native models provide a means of saving
        # Saves a folder containing model at directory/self.Model_Name
        # all goose-native models save a model_identification.json file with "Model Type"
            # for knowing what model class it is a product of
    @abstractmethod
    def Save_Model(self, directory):
        pass

    # all goose-native models provide a means of loading
        # to load, model must be collectivley stored as one folder
    @abstractmethod
    def Load_Model(self, path):
        pass