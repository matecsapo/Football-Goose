# for implementing a data type
from goose.data.data_types import Data_Type
from typing import Callable, Any

# for retrieving results data
import soccerdata as sd
from goose.data.goose_data_structures.identifiers import Team, League, Season

# Data types results_data, defined as data of/on completed games (i.e., scores of completed games)
results_data = Data_Type.Create_Type("Results Data", Callable[[League, Season], Any], "Data on completed games")

# Data retrieval function for retrieving results data via understats via soccerdata
@results_data.Define_Data_Retrieval_Function("UnderStats", "Retrieves results data via Understats via soccerdata")
def retrieve_results_understats(league : League, season : Season):
        # pull results data
        us = sd.Understat(leagues=league.to_soccerdata_name(), seasons=season.to_soccerdata_tag(), proxy=None, no_cache=False, no_store=False)
        results = us.read_team_match_stats(force_cache = False)
        # standardize team names
        results["home_team"] = results["home_team"].apply(Team)
        results["away_team"] = results["away_team"].apply(Team)        
        return results

# Set UnderStats as default results retrieval source
results_data.Set_Source("UnderStats")