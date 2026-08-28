# for data manipulation / storage
from goose.data.goose_data_structures.identifiers import Team
from datetime import datetime
import pandas as pd
from pathlib import Path
from typing import Generic, TypeVar

# struct for storing a specific game
class Game:
    # Game consists of home_team, away_team, and game date
    # flag indicating whether game is at a neutral venue
    def __init__(self, home_team : Team, away_team : Team, date : datetime, neutral_venue : bool = False):
        self.home_team = home_team
        self.away_team = away_team
        self.date = date
        self.neutral_venue = neutral_venue

    # to dictionary
    def to_dictionary(self):
        return (
            {
                "home_team": self.home_team,
                "away_team": self.away_team,
                "date": self.date,
                "neutral_venue" : self.neutral_venue
            })

    # to dataframe
    def to_dataframe(self):
        return pd.DataFrame([self.to_dictionary()])

    # save
    def save(self, path):
        self.to_dataframe().to_csv(Path(path) / Path(f"{self.home_team}(h)_vs._{self.away_team}(a).csv"))

    # view
    def view(self):
        print(self.to_dataframe())  

# struct for storing a specific completed game
class Completed_Game(Game):
    # extends to include home_goals, away_goals
    def __init__(self, home_team : Team, away_team : Team, date : datetime, 
                 home_goals : int, away_goals : int, home_xg : int = None, away_xg : int = None,
                 neutral_venue : bool = False):
        super().__init__(home_team, away_team, date, neutral_venue)
        self.home_goals = home_goals
        self.away_goals = away_goals
        self.home_xg = home_xg
        self.away_xg = away_xg

    # to dictionary
    def to_dictionary(self):
        return (
            {
                "home_team": self.home_team,
                "away_team": self.away_team,
                "date": self.date,
                "neutral_venue" : self.neutral_venue,
                "home_goals" : self.home_goals,
                "away_goals" : self.away_goals,
                "home_xg" : self.home_xg,
                "away_xg" : self.away_xg
            })     

# struct for storing a simluation of a specific game
class Game_Simulation(Game):
    # extends to include home_goals, away_goals
    def __init__(self, game : Game, home_simulated_goals : int, away_simulated_goals : int):
        super().__init__(game.home_team, game.away_team, game.date, game.neutral_venue)
        self.home_simulated_goals = home_simulated_goals
        self.away_simulated_goals = away_simulated_goals

    # to dictionary
    def to_dictionary(self):
        return (
            {
                "home_team": self.home_team,
                "away_team": self.away_team,
                "date": self.date,
                "neutral_venue" : self.neutral_venue,
                "home_simulated_goals" : self.home_simulated_goals,
                "away_simulated_goals" : self.away_simulated_goals
            })  

# struct for storing a prediction for a specific game
class Game_Prediction(Game):
    # extends to include home/away predicted goals, prob of home win / draw / away win
    def __init__(self, game : Game,
                 home_pred_goals : float, away_pred_goals : float,
                 prob_home_win : float, prob_away_win : float, prob_draw : float):
        super().__init__(game.home_team, game.away_team, game.date, game.neutral_venue)
        self.home_pred_goals = home_pred_goals
        self.away_pred_goals = away_pred_goals
        self.prob_home_win = prob_home_win
        self.prob_away_win = prob_away_win
        self.prob_draw = prob_draw

    # to dictionary
    def to_dictionary(self):
        return (
            {
                "home_team": self.home_team,
                "away_team": self.away_team,
                "date": self.date,
                "neutral_venue" : self.neutral_venue,
                "home_pred_goals" : self.home_pred_goals,
                "away_pred_goals" : self.away_pred_goals,
                "prob_home_win" : self.prob_home_win,
                "prob_away_win" : self.prob_away_win,
                "prob_draw" : self.prob_draw
            })      

# struct for storing a points expectation for a specific game
class Game_Points_Expectation(Game):
    def __init__(self, game : Game,
                 home_xPts : float, away_xPts):
        super().__init__(game.home_team, game.away_team, game.date, game.neutral_venue)
        self.home_xPts = home_xPts
        self.away_xPts = away_xPts

    # to dictionary
    def to_dictionary(self):
        return (
            {
                "home_team": self.home_team,
                "away_team": self.away_team,
                "date": self.date,
                "neutral_venue" : self.neutral_venue,
                "home_xPts" : self.home_xPts,
                "away_xPts" : self.away_xPts
            }
        )

# struct for storing a set/schedule of games, uncompleted, to be completed, or else
# ordered by date (earliest to latest)
# parameterized for specifying type of games contained
G = TypeVar('G', bound='Game')
class Games(Generic[G]):
    # Can be constructed as an empty list of games, one game, or list of games
    def __init__(self, games : None | G | list[G]):
        if games == None:
            self.games = []
        elif isinstance(games, list):
            self.games = games
        else:
            self.games = [games]
        # sort by date order immediately
        self.Date_Order()
    
    # Adding one game to set
    def Add_Game(self, game : G):
        self.games.append(game)
        self.Date_Order()

    # Adding list of games to set
    def Add_Games(self, games : list[G]):
        self.games.extend(games)
        self.Date_Order()

    # Order games by date
    def Date_Order(self):
        self.games.sort(key = (lambda x : x.date))

    # returns list of all games as a dataframe
    def to_dataframe(self):
        return pd.DataFrame( 
            [g.to_dictionary() for g in self.games]
        )

    # save
    def save_data(self, path):
        self.to_dataframe().to_csv(path)

    # view
    def view_data(self):
        print(self.to_dataframe().head(20))