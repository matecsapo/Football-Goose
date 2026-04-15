from pathlib import Path
import json
# all goose-native models
from goose.models.goose_model import Goose_Model
from goose.models.static_poi_reg_model import Static_Poi_Reg_Model


# Returns storage path of goose's trained models for loading them
def get_path(goose_trained_model_name):
    return Path(__file__).parent / goose_trained_model_name

# all goose-native models store a model_identification.json file with field "Model Type"
# this mapping defines "Model Type" --> the model class it is a model of
model_type_mapping = {
    "Static Poisson Regression Model" : Static_Poi_Reg_Model
}

# for loading built-in, goose_trained_models from goose.models.goose_trained_models
# returns object of type of model (i.e. Static_Poi_Reg_Model)
def Load_Goose_Trained_Model(goose_trained_model_name):
    # Retrieve path of goose_trained_model_name
    path = get_path(goose_trained_model_name)
    # Determine model type of goose_trained_model_name
    model_type = None
    with open(path/"model_identification.json", "r") as f:
        model_type = json.load(f)["Model Type"]
    target_model_class = model_type_mapping[model_type]
    # Load goose_trained_model_name as instance of it's model_class
    goose_trained_model = target_model_class(goose_trained_model_name)
    goose_trained_model.Load_Model(path)
    return goose_trained_model