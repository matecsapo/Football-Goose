# for creaeting an abstract class standardizing data pulling
from abc import ABC, abstractmethod
from typing import Callable, Any

# for data manipulation / storage
import pandas as pd
from datetime import datetime, timezone
from goose.data.goose_data_structures import Game, Games, League_Table

# soccerdata api used to pull all data
import soccerdata as sd

# for renaming teams to a common set of names
from goose.name_standardization import standardize_team_names

# Source_Data defines a means of pulling source/raw data via Goose
# By default, Source_Data (Results_Data, Standings_Data, and Schedule_Data) wrap around soccerdata api to pull desired data
# source/means of pulling data can be overrided to custom functions via Set_Source functions
# pulled/retrieved data is stored into self.data
class Source_Data(ABC):
    # Initialized by [league, season] to pull data of
    def __init__(self, leagues, seasons):
        self.leagues = leagues
        self.seasons = seasons
        # for storing retrieved data
        self.data = None

    # static var storing function/means of pulling data
    # by default, gets set as the subclasses retrieve_data_default
    retrieve_data_function : callable = None

    # default function/means of pulling data
    @abstractmethod
    def retrieve_data_default(self, leagues, seasons):
        pass

    # for setting pull_data function to specified function
    @classmethod
    @abstractmethod
    def set_source(self, function):
        pass

    # for setting pull_data function to default
    @classmethod
    @abstractmethod
    def set_source_default(self):
        pass

    # Save data
    def save_data(self, path):
        pass

    # View data
    def view_data(self):
        pass

# Results Data of specific [leagus, seasons]'s results (incl. xg)
class Results_Data(Source_Data):
    # default means of pulling requested [league, seasons]'s results
        # default = UnderStats via soccerdata
    def retrieve_data_default(self, leagues, seasons):
        us = sd.Understat(leagues=leagues, seasons=seasons, proxy=None, no_cache=False, no_store=False)
        results = us.read_team_match_stats(force_cache = False)
        # standardize team names
        results["home_team"] = standardize_team_names(results["home_team"])
        results["away_team"] = standardize_team_names(results["away_team"])
        return results

    # set default retrieve_data_function
    retrieve_data_function = retrieve_data_default

    # Initialized by [league, season] to pull results data of
    def __init__(self, leagues, seasons):
        super().__init__(leagues, seasons)
        # pull results data according to selected function
        self.data = self.retrieve_data_function(self.leagues, self.seasons)

    # sets retrieve_data_functon to specified function
    @classmethod
    def set_source(self, function : Callable[[str, str], Any]):
        self.retrieve_data_function = function

    # Set retrieve_data_function to default
    @classmethod
    def set_source_default(self):
        self.retrieve_data_function = self.retrieve_data_default
    
    # save data
    def save_data(self, path):
        self.data.to_csv(path)

    # view data
    def view_data(self):
        print(self.data.head(20))

# Standings Data (via SofaScore)
class Standings_Data(Source_Data):
    # default means of pulling requested [league, season]'s results
        # default = SofaScore via soccerdata
    def retrieve_data_default(self, leagues, seasons):
        sfs = sd.Sofascore(leagues=leagues, seasons=seasons, proxy=None, no_cache=False, no_store=False)
        standings = sfs.read_league_table(force_cache = False)
        # just in case, sort by (points, goal diff)
        standings = standings.sort_values(by = ["Pts", "GD"], ascending = False)
        # uppercase team
        standings = standings.rename(columns = {"team" : "Team"})
        # standardize team names
        standings["Team"] = standardize_team_names(standings["Team"])
        standings = League_Table(standings)
        return standings
    
    # set default retrieve_data_function
    retrieve_data_function = retrieve_data_default

    # Initialized by [league, seasons] to pull standings data of
    # Standings_Data must be stored into a Standings schema pd dataframe
    def __init__(self, leagues, seasons):
        super().__init__(leagues, seasons)
        # enforce self.data as a League_Table object
        self.data : League_Table = None
        # # pull standings data according to selected function
        self.data = self.retrieve_data_function(self.leagues, self.seasons)

    # sets retrieve_data_functon to specified function
    @classmethod
    def set_source(self, function : Callable[[str, str], League_Table]):
        self.retrieve_data_function = function

    # Set retrieve_data_function to default
    @classmethod
    def set_source_default(self):
        self.retrieve_data_function = self.retrieve_data_default
    
    # Save data
    def save_data(self, path):
        self.data.save(path)

    # view data
    def view_data(self):
        self.data.view()

# Schedule Data (via ESPN)
class Schedule_Data(Source_Data):
    # default means of pulling requested [league, season]'s schedule data
        # default = ESPN via soccerdata
    def retrieve_data_default(self, leagues, seasons, upcoming_only):
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
    
    # set default retrieve_data_function
    retrieve_data_function = retrieve_data_default

    # Initialized by [league, season, upcoming games only?] to pull Schedule data of
    def __init__(self, leagues, seasons, upcoming_only):
        super().__init__(leagues, seasons)
        # whether or not to pull only games yet to happen
        self.upcoming_only = upcoming_only
        # enforce that self.data must be stored as a Games object
        self.data : Games = None
        # pull schedule data accordig to selected function
        self.data = self.retrieve_data_function(self.leagues, self.seasons, self.upcoming_only)
    
    # sets retrieve_data_function to specified function
    @classmethod
    def set_source(self, function : Callable[[str, str], Games]):
        self.retrieve_data_function = function

    # Set retrieve_data_function to default
    @classmethod
    def set_source_default(self):
        self.retrieve_data_function = self.retrieve_data_default

    # Save data
    def save_data(self, path):
        self.data.save_data(path)
    
    # view data
    def view_data(self):
        self.data.view_data()


