# for data manipulation
import pandas as pd
import json
from datetime import datetime, timezone
from pathlib import Path

# soccerdata api used to pull all data
import soccerdata as sd

# for renaming teams to a common set of names
from goose.name_standardization import standardize_team_name, standardize_team_names

# Results Data (via UnderStats) of specific [leagus, seasons]'s results (incl. xg)
class Results_Data:
    # Initialize by pulling requested [leagues, seasons]'s results
    def __init__(self, leagues, seasons):
        self.leagues = leagues # specified leagues
        self.seasons = seasons # specified seasons 
        # retrieve the specified data
        self.data = None
        self.pull_results(leagues, seasons)

    # pulls and caches requeusted [leagues, seasons]'s results (incl. xg) data via understats
    def pull_results(self, leagues, seasons):
        us = sd.Understat(leagues=leagues, seasons=seasons, proxy=None, no_cache=False, no_store=False)
        self.data = us.read_team_match_stats(force_cache = False)
        # standardize team names
        self.data["home_team"] = standardize_team_names(self.data["home_team"])
        self.data["away_team"] = standardize_team_names(self.data["away_team"])
    
    # save data
    def save_data(self, path):
        self.data.to_csv(path)

    # view data
    def view_data(self):
        print(self.data.head(20))

# Standings Data (via SofaScore)
class Standings_Data:
    # Initialize by pulling requested [leagues, seasons]'s standings
    def __init__(self, leagues, seasons):
        self.leagues = leagues # specified leagues
        self.seasons = seasons # specified seasons 
        # retrieve the specified data
        self.data = None
        self.pull_standings(leagues, seasons)

    # pulls and caches requested [leagues, seasons]'s standings data via sofascore
    def pull_standings(self, leagues, seasons):
        sfs = sd.Sofascore(leagues=leagues, seasons=seasons, proxy=None, no_cache=False, no_store=False)
        self.data = sfs.read_league_table(force_cache = False)
        # just in case, sort by (points, goal diff)
        self.data = self.data.sort_values(by = ["Pts", "GD"], ascending = False)
        # uppercase team
        self.data = self.data.rename(columns = {"team" : "Team"})
        # standardize team names
        self.data["Team"] = standardize_team_names(self.data["Team"])
    
    # Simplifies standings to just [team, matches played, points, goal diff], ordered by (points, goal diff)
    def Simplify(self):
        # stop team from being index
        self.data = self.data.reset_index()
        self.data = self.data[["Team", "MP", "Pts", "GD"]]
    
    # Save data
    def save_data(self, path):
        self.data.to_csv(path)

    # view data
    def view_data(self):
        print(self.data.head(20))

# Schedule Data (via ESPN)
class Schedule_Data:
    # Initialized by pulling requeusted [leagues, seasons]'s schedule
    # upcoming_only includes only games yet to be played
    def __init__(self, leagues, seasons, upcoming_only):
        self.leagues = leagues # specified leagues
        self.seasons = seasons # specified seasons 
        self.upcoming_only = upcoming_only # whether or not only games yet to be played
        # retrieve the specified data
            # data is stored as a Games object
        self.data : Games = None
        # data is also stored as the raw csv table
        self.raw_data = None
        self.pull_schedule(leagues, seasons, upcoming_only)

    # pulls and caches requested [leagues, season]s standings data via 
    def pull_schedule(self, leagues, seasons, upcoming_only):
        espn = sd.ESPN(leagues=leagues, seasons=seasons, proxy=None, no_cache=False, no_store=False)
        self.raw_data = espn.read_schedule(force_cache = False)
        # Convert date strings to datetime objects
        self.raw_data['date'] = pd.to_datetime(self.raw_data['date'])
        # standardize team names
        self.raw_data["home_team"] = standardize_team_names(self.raw_data["home_team"])
        self.raw_data["away_team"] = standardize_team_names(self.raw_data["away_team"])
        # if requested, filter to only games yet to be played
        if upcoming_only:
            self.raw_data = self.raw_data[self.raw_data["date"] > datetime.now((timezone.utc))]
        # Package schedule of games into a Games object
        games_list = []
        for _, row in self.raw_data.iterrows():
            games_list.append(Game(
                home_team = row["home_team"],
                away_team = row["away_team"],
                date = row["date"]
            ))
        self.data = Games(games_list)

    # Save data
    def save_data(self, path):
        self.raw_data.to_csv(path)
    
    # view data
    def view_data(self):
        print(self.raw_data.head(20))

# struct for storing contents of a PL game
class Game:
    # Game consists of home_team, away_team, and game date
    def __init__(self, home_team, away_team, date : datetime):
        self.home_team = home_team
        self.away_team = away_team
        self.date = date

# struct for storing a set/schedule of games
    # ordered by date (earliest to latest)
class Games:
    # Can be constructed as an empty list of games, one game, or list of games
    def __init__(self, games : None | Game | list[Game]):
        if games == None:
            self.games = []
        elif isinstance(games, list):
            self.games = games
        else:
            self.games = [games]
        # sort by date order immediately
        self.Date_Order()
    
    # Adding one game to set
    def Add_Game(self, game : Game):
        self.games.append(game)
        self.Date_Order()

    # Adding list of games to set
    def Add_Games(self, games : list[Game]):
        self.games.extend(games)
        self.Date_Order()

    # Order games by date
    def Date_Order(self):
        self.games.sort(key = (lambda x : x.date))

# struct for match prediction report
class Game_Prediction:
    # Consists of Game, and various predictions
    # Stores data as a dictionary for ease of use
    def __init__(self, game : Game, home_xg, away_xg, prob_home_win, prob_away_win, prob_draw):
        self.game = game
        self.home_xg = home_xg
        self.away_xg = away_xg
        self.prob_home_win = prob_home_win
        self.prob_away_win = prob_away_win
        self.prob_draw = prob_draw
        # store all data as a dataframe for simplicity
        self.prediction = {"game" : f"{game.home_team}(h) vs. {game.away_team}(a)",
                            f"{game.home_team} xg" : home_xg,
                            f"{game.away_team} xg" : away_xg,
                            f"{game.home_team} Win Probability" : prob_home_win,
                            f"{game.away_team} Win Probability" : prob_away_win,
                            f"Draw Probability" : prob_draw}

    # returns game_predict as a dictionary
    def to_dict(self):
        return {
            "home_team": self.game.home_team,
            "away_team": self.game.away_team,
            "date": self.game.date,
            "home_xg": self.home_xg,
            "away_xg": self.away_xg,
            "p_home": self.prob_home_win,
            "p_away": self.prob_away_win,
            "p_draw": self.prob_draw
        }
    
    # returns game_prediction as a pd dataframe
    def to_dataframe(self):
        return pd.DataFrame([self.to_dict()])
    
    # save
    def save(self, path):
        self.to_dataframe().to_csv(Path(path) / Path(f"{self.game.home_team}(h)_vs._{self.game.away_team}(a)_prediction.csv"))

    # view
    def view(self):
        print(self.to_dataframe())
