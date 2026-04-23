# stop all logging happening
import logging
logging.disable(logging.CRITICAL)
import os
os.environ["SOCCERDATA_LOGLEVEL"] = "CRITICAL"

from .model import Model
from .data import Results_Data, Standings_Data, Schedule_Data, Game, Games, Game_Prediction
from .name_standardization import standardize_league_name, standardize_league_names, standardize_team_name, standardize_team_names
