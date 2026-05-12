# stop all logging happening
import logging
logging.disable(logging.CRITICAL)
import os
os.environ["SOCCERDATA_LOGLEVEL"] = "CRITICAL"

from .model import Model
from .data.goose_data_structures import Game, Games, Game_Prediction
from .data.built_in_data_types.results_data import results_data
from .data.built_in_data_types.standings_data import standings_data
from .data.built_in_data_types.schedule_data import schedule_data