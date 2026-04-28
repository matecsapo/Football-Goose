# for implementing a data type
from goose.data.data_types import Data_Type
from typing import Callable, Any
import pandas as pd

# for retrieving schedule data
import soccerdata as sd
from goose.name_standardization import standardize_team_names

# for storing pulled schedule
from goose.data.goose_data_structures import Game, Games
from datetime import datetime, timezone

# Data type schedule_data, defined as data of schedule of games/league/competition
schedule_data = Data_Type.Create_Type("Schedule Data", Callable[[str, str, bool], Games], "Data on scheduling of games")

# Data retrieval function for retrieving schedule data via ESPN via soccerdata
@schedule_data.Define_Data_Retrieval_Function("ESPN", "Retrieves schedule data via ESPN via soccerdata")
def retrieve_schedule_espn(leagues, seasons, upcoming_only):
        # retrieve schedule data
        espn = sd.ESPN(leagues=leagues, seasons=seasons, proxy=None, no_cache=False, no_store=False)
        schedule = espn.read_schedule(force_cache = False)
        # Convert date strings to datetime objects
        schedule['date'] = pd.to_datetime(schedule['date'])
        # standardize team names
        schedule["home_team"] = standardize_team_names(schedule["home_team"])
        schedule["away_team"] = standardize_team_names(schedule["away_team"])
        # if requested, filter to only games yet to be played
        if upcoming_only:
            schedule = schedule[schedule["date"] > datetime.now((timezone.utc))]
        # Package schedule of games into a Games object
        games_list = []
        for _, row in schedule.iterrows():
            games_list.append(Game(
                home_team = row["home_team"],
                away_team = row["away_team"],
                date = row["date"]
            ))
        games = Games(games_list)
        return games

# Set ESPN as default schedule data retrieval source
schedule_data.Set_Source("ESPN")