# for implementing a data type
from goose.data.data_types import Data_Type
from typing import Callable, Any

# for retrieving standings data
from goose.data.goose_data_structures import Standings, League_Table
import soccerdata as sd
from goose.name_standardization import standardize_team_names
import pandas as pd

# Data type standings_data, defined as data of/on standings for a given [league, season]
standings_data = Data_Type.Create_Type("Standings Data", Callable[[str, str], Standings], "Standings data for a given [league, season]")

# Data retrieval function for retrieving standings data via sofascore via soccerdata
@standings_data.Define_Data_Retrieval_Function("Sofascore", "Retrieves standings data via sofascore via soccerdata")
def retrieve_standings_sofascore(leagues, seasons):
        # retrieve standings data
        sfs = sd.Sofascore(leagues=leagues, seasons=seasons, proxy=None, no_cache=False, no_store=False)
        standings = sfs.read_league_table(force_cache = False)
        # just in case, sort by (points, goal diff)
        standings = standings.sort_values(by = ["Pts", "GD"], ascending = False)
        # uppercase team
        standings = standings.rename(columns = {"team" : "Team"})
        # standardize team names
        standings["Team"] = standardize_team_names(standings["Team"])
        # Store standings data into Goose-standardized structure 
        standings = League_Table(standings)
        return standings

# Data retrieval function for retrieving standings data via understats (reconstructio) via soccerdata
# this approach determines current standings by "summing" all games completed so far this season
@standings_data.Define_Data_Retrieval_Function("Understats(Reconstruction)", "Retrieves standings data via understats (reconstruction) via soccerdata")
def retrieve_standings_understats_reconstruction(league, season) -> League_Table:
        # retrieve results data
        us = sd.Understat(league, season, proxy=None, no_cache=False, no_store=False)
        data = us.read_team_match_stats()
        # rename columns
        home = data[['home_team', 'home_points', 'home_goals', 'away_goals']].rename(
            columns={'home_team': 'Team', 'home_points': 'Pts', 'home_goals': 'GF', 'away_goals': 'GA'}
        )
        away = data[['away_team', 'away_points', 'away_goals', 'home_goals']].rename(
            columns={'away_team': 'Team', 'away_points': 'Pts', 'away_goals': 'GF', 'home_goals': 'GA'}
        )
        # Construct standings by "summing" all played games
        table = pd.concat([home, away]).groupby('Team').agg(
            MP=('Pts', 'count'),
            Pts=('Pts', 'sum'),
            GF=('GF', 'sum'),
            GA=('GA', 'sum')
        ).reset_index()
        table['GD'] = table['GF'] - table['GA']
        standings = table[['Team', 'MP', 'Pts', 'GD']].sort_values(
            by=['Pts', 'GD'], ascending=False
        ).reset_index(drop=True)
        # Store standings data into Goose-standardized structure
        standings = League_Table(standings)
        return standings

# Set Sofascore as default standings retrieval source
standings_data.Set_Source("Sofascore")
