from abc import ABC, abstractmethod
from typing import Self

# for data storage
from goose.data import Game, Game_Prediction
from pathlib import Path
import os
import sys
import json
from datetime import datetime
import subprocess
import dill

# Abstract class defining operations required to be provided by all models
# For a model to be compatible with goose.engine, it must be a subclass of Model
# Technically, Save_Model_Data() and Factory_Load_Model() are only required to allow for compatability with goose.engine.easy_predict
    # if model works/saves/loads very differently than pattern below, just define blank/do-nothing concrete implementations of both functions
class Model(ABC):
    # all models must have a field self.Model_Name
    def __init__(self, model_name):
        self.Model_Name = model_name

    # Predict specified game according to model
    @abstractmethod
    def Predict_Game(self, game : Game) -> Game_Prediction:
        pass

    # Simulate specified game according to model
    @abstractmethod
    def Simulate_Game(self, game : Game) -> tuple[int, int]:
        pass
    
    # saves all necessary model-specific save/data/files into model_save_root self.Model_Name/
    # implementing save_model() specifies model-specific save behaviour
    def save_model(self, model_save_root : str | Path):
        pass

    # model-specific factory method for loading models from model_save_path self.Model_Name/
    # implementing load_model() specifies model-specific load behabviour
    @classmethod
    def load_model(cls, model_save_path : str | Path) -> Self:
        pass

    # Saves a football-goose compatible model (concrete subclass of Model) to directory/[self.Model_Name]/
    # stores a .fgm save of model at directory/[self.Model_Name]/[self.Model_Name].fgm
    # .fgm format is defined as a [folder].fgm consisting of:
        # model_identification.json file with model type, timestamp, model root save path = directory/[self.Model_Name]
        # environment.txt defining python environment
        # model.bin, a dill save of the Model object
    # This function allows for a generalized process of storing and loading any football-goose compatible models
        # Primarily, this allows for integration with goose.engine.easy_predict
    # calls model-specific save_model(directory/[self.Model_Name]) to include model-specific saving behaviour
    def save_model_fgm(self, directory : str):
        directory = Path(directory)
        # model's root save path
        model_root = directory / self.Model_Name
        os.makedirs(model_root, exist_ok = True)
        # Folder for storing model's .fgm file
        fgm_folder = model_root / (self.Model_Name + ".fgm")
        os.makedirs(fgm_folder, exist_ok = True)
        # save model identification @ [self.Model_Name].fgm/model_identification.json (model type, imestamp saved, model root save path)
        model_type = self.__class__.__name__
        with open(fgm_folder / "model_identification.json", "w") as f:
            json.dump({
                "Model Type" : model_type,
                "Timestamp Trained" : datetime.now().isoformat(),
                "Model Root Save Path": str(model_root.absolute())
            }, f, indent = 4)
        # save python environment info
        with open(fgm_folder / "environment.txt", "w") as f:
            subprocess.run(['pip', 'freeze'], stdout=f, text=True)
        # save dill dump of Model object @ model.bin
        with open(fgm_folder / "model.bin", "wb") as f:
            dill.dump(self, f)
        # Invoke model-specific saving behaviour
        self.save_model(model_root)

    # factory model to load a .fmg file storing a football-goose compatible model (concrete subclass of Model)
    # Returns an the concrete-subclassclass-of-Model object of the stored model
    # This function allows for a generalized process of storing and loading any football-goose compatible models
        # Primarily, this allows for integration with goose.engine.easy_predict
    # as fallback, if loading via .fgm file fails, defaults to using model-specific load_model() process
    # attempt_fgm_load controls whether to even attempt fgm load, or just only attempt model-specific load
    @classmethod
    def load_model_fgm(cls, fgm_path : str | Path, attempt_fgm_load : bool = True) -> Self:
        fgm_path = Path(fgm_path)
        model = None
        # if fgm load attempt requested, attempt to load model via the model.bin
        if attempt_fgm_load:
            try:
                with open(fgm_path / "model.bin", "rb") as f:
                    model = dill.load(f)
                return model
            # if loading fails, just proceed to fallback
            except Exception:
                pass
        # as fall-back / if requested, load via model-specific load_model() definition
        # determine model definition and full model path
        model_class_name = None
        model_root_save_path = None
        with open(fgm_path / "model_identification.json") as f:
            model_identification = json.load(f)
            model_class_name = model_identification["Model Type"]
            model_root_save_path = model_identification["Model Root Save Path"]
        # pull required class reference
        import goose.registry as registry
        model_class, _ = registry.model_definitions[model_class_name]
        # load model via model-specific load_model()
        model = model_class.load_model(model_root_save_path)
        return model
    
    # Decorator hook for adding user-defined models into goose's registry
    @staticmethod
    def define_model(name : str = None, description : str = None):
        import goose.registry as registry
        def add_model_to_registry(cls):
            registry.model_definitions[cls.__name__ if name == None else name] = (cls, description)
            return cls
        return add_model_to_registry