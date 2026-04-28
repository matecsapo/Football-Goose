# for implementing a data type
from goose.data.data_types import Data_Type
from typing import Callable, Any

# for retrieving results data
import soccerdata as sd
from goose.name_standardization import standardize_team_names

# Data types results_data, defined as data of/on completed games (i.e., scores of completed games)
results_data = Data_Type.Create_Type("Results Data", Callable[[str, str], Any], "Data on completed games")

# Data retrieval function for retrieving results data via understats via soccerdata
@results_data.Define_Data_Retrieval_Function("UnderStats", "Retrieves results data via Understats via soccerdata")
def retrieve_results_understats(leagues, seasons):
        # pull results data
        us = sd.Understat(leagues=leagues, seasons=seasons, proxy=None, no_cache=False, no_store=False)
        results = us.read_team_match_stats(force_cache = False)
        # standardize team names
        results["home_team"] = standardize_team_names(results["home_team"])
        results["away_team"] = standardize_team_names(results["away_team"])
        return results

# Set UnderStats as default results retrieval source
results_data.Set_Source("UnderStats")