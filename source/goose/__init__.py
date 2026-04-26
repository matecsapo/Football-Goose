# stop all logging happening
import logging
logging.disable(logging.CRITICAL)
import os
os.environ["SOCCERDATA_LOGLEVEL"] = "CRITICAL"

from .model import Model
from .data.goose_data_structures import Game, Games, Game_Prediction
from .data.pull_data import Results_Data, Standings_Data, Schedule_Data
from .name_standardization import standardize_league_name, standardize_league_names, standardize_team_name, standardize_team_names
