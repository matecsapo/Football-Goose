# utilities.py has some helpers commonly used by goose operations

# imports necessary for helpers
from goose.model import Model
from goose.forecast.league_monte_carlo_simulation import PL_Monte_Carlo_Simulation, Laliga_Monte_Carlo_Simulation, Bundesliga_Monte_Carlo_Simulation, Ligue1_Monte_Carlo_Simulation, SerieA_Monte_Carlo_Simulation
from pathlib import Path

# for discovering models
from goose.discover import discover_models

# goose_operations wide helper function to load specified model
def load_model(model_name : str) -> tuple[Model, str]: # model and model_name
    # re-run discover_models() to identify any newly added (by just-run operation(s)) models
    discover_models()
    # retrieve model_path by model_name from registry
    import goose.registry as registry
    model_path = registry.models_registry.retrieve_path(model_name)
    # load model via model_path .fgm file folder
    model = Model.load_model_fgm(model_path)
    # return (model, model_name)
    return model, model_name

# goose_operations wide definition of defeault models to use per league
league_MC_mappings = {
    "ENG-Premier League": PL_Monte_Carlo_Simulation,
    "ESP-La Liga": Laliga_Monte_Carlo_Simulation,
    "GER-Bundesliga": Bundesliga_Monte_Carlo_Simulation,
    "FRA-Ligue 1": Ligue1_Monte_Carlo_Simulation,
    "ITA-Serie A": SerieA_Monte_Carlo_Simulation
}