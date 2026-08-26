# for data manipulation / storage
from goose.data.goose_data_structures.identifiers import Team
from datetime import datetime
import pandas as pd
from pathlib import Path

# struct for storing a specific game
class Game:
    # Game consists of home_team, away_team, and game date
    # flag indicating whether game is at a neutral venue
    def __init__(self, home_team : Team, away_team : Team, date : datetime, neutral_venue : bool = False):
        self.home_team = home_team
        self.away_team = away_team
        self.date = date
        self.neutral_venue = neutral_venue

# struct for storing a specific completed game
class Completed_Game(Game):
    # extends to include home_goals, away_goals
    def __init__(self, home_team : Team, away_team : Team, date : datetime, home_goals : int, away_goals : int, neutral_venue : bool = False):
        super().__init__(home_team, away_team, date, neutral_venue)
        self.home_goals = home_goals
        self.away_goals = away_goals

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

    # returns list of all games as a dataframe
    def to_dataframe(self):
        return pd.DataFrame(
            {
                "home_team": g.home_team,
                "away_team": g.away_team,
                "date": g.date
            } 
            for g in self.games
        )

    # save
    def save_data(self, path):
        self.to_dataframe().to_csv(path)

    # view
    def view_data(self):
        print(self.to_dataframe().head(20))

# struct for storing match prediction report
# Consts of:
    # Game,
    # home/away xg, prob of home win / draw / away win
class Game_Prediction:
    def __init__(self, game : Game, home_xg, away_xg, prob_home_win, prob_away_win, prob_draw):
        self.game = game
        self.home_xg = home_xg
        self.away_xg = away_xg
        self.prob_home_win = prob_home_win
        self.prob_away_win = prob_away_win
        self.prob_draw = prob_draw

    # returns game_predict as a dictionary
    def to_dict(self):
        return {
            "home_team": self.game.home_team.team,
            "away_team": self.game.away_team.team,
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