# for defining data structures
import pandas as pd
import pandera.pandas as pa
from datetime import datetime
from pathlib import Path
from abc import ABC

# for standardizing team names
from goose.data.name_standardization import Team_Name_Mappings, League_Name_Mappings

# goose_data_structures.py defines some standardized data structures that must be abided to
#   to allow for interaction with the Football-Goose engine

# struct for storing a specific team
class Team:
    # upon initialized, adjusts team name to standardized Goose equivalent
    def __init__(self, team_name : str):
        self.team = self.standardize_team_name(team_name)

    # Return the standardized name according to provided alias
    @staticmethod
    def standardize_team_name(alias : str):
        return Team_Name_Mappings[alias]

    # Standardizes team names from various aliases used by sources to chosen set of names
    @staticmethod
    def standardize_team_names(team_names : pd.Series):
        return team_names.map(Team_Name_Mappings).fillna(team_names)
    
    # equivalence of teams
    def __eq__(self, other):
        if not isinstance(other, Team):
            return False
        return self.team == other.team
    
    # string alphabetical ordering of teams
    def __lt__(self, other):
        if not isinstance(other, Team):
            return NotImplemented
        return self.team < other.team
    
    # hashing
    def __hash__(self):
        return hash(self.team)
    
    # for df printing
    def __repr__(self):
        return self.team

    # For print() and CSV exports
    def __str__(self):
        return self.team
    
# struct for storing a specific league
class League:
    # upon initialization, adjusts league name to standardized Goose equivalent
    def __init__(self, league_name : str):
        self.league = self.standardize_league_name(league_name)

    # Return the standardized league name according to provided alias
    @staticmethod
    def standardize_league_name(alias : str):
        return League_Name_Mappings[alias]

    # standardize league names from various aliases used by sources to chosen set of names
    @staticmethod
    def standardize_league_names(league_names : pd.Series):
        return league_names.map(League_Name_Mappings).fillna(league_names)

    # equivalence of league
    def __eq__(self, other):
        if not isinstance(other, League):
            return False
        return self.league == other.league
    
    # hashing
    def __hash__(self):
        return hash(self.league)
    
    # for df printing
    def __repr__(self):
        return self.league

    # For print() and CSV exports
    def __str__(self):
        return self.league

# struct for storing a specific game
class Game:
    # Game consists of home_team, away_team, and game date
    # flag indicating whether game is at a neutral venue
    def __init__(self, home_team : Team, away_team : Team, date : datetime, neutral_venue = False):
        self.home_team = home_team
        self.away_team = away_team
        self.date = date
        self.neutral_venue = neutral_venue

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

# struct for storing a given competition's standings
# Abstracted - implemented for various concrete competition styles (i.e. round-robin, KO, etc.)
# standings are stored in self.standings
class Standings(ABC):
    # Standings must specify [league, season]
    def __init__(self, league : League = None, season = None):
        self.league = league
        self.season = season
        # for storing [league, season]'s standings
        self.standings = None
    
    # save
    def save(self, path):
        pass

    # view
    def view(self):
        pass

# struct for storing table-style standings
# Abstracted - implemented for specific type of tabled standings
# Tables store standings as pd dataframe satisfiying specified schema
class Table(Standings, ABC):
    # pd dataframe schema
    # each concrete Table standings table type implements
    Table_Schema : pa.DataFrameSchema = None

    # Constructed by immediately validating supplied dataframe according to pandera league table schema
    def __init__(self, league_table : pd.DataFrame, league : League = None, season = None):
        super().__init__(league, season)
        # Enforce league_table as being of required League_Table_Schema pd dataframe schema
        self.standings : pd.DataFrame = league_table
        self.standings = self.Table_Schema.validate(self.standings)

    # sipmlifies standings to just rows of Table_Schem
    def simplify(self):
        self.standings = self.standings[list(self.Table_Schema.columns.keys())]

    # save data
    def save(self, path):
        self.standings.to_csv(path)
    
    # view data
    def view(self):
        print(self.standings.head(20))

# struct for storing a given [league, season] league=round-robin - style-competition standings
# A League_Table must have:
    # Team, MP, Pts, GD
    # Can have any additional columns, as desired
class League_Table(Table):
    # Pandera schema defining league tabble daf
    Table_Schema = pa.DataFrameSchema(
        columns = {
            "Team": pa.Column(object),
            "MP":   pa.Column(int, pa.Check.ge(0)), # MP must be >= 0
            "Pts":  pa.Column(int, pa.Check.ge(0)), # Pts must be >= 0
            "GD":   pa.Column(int),
        },
        # Additional columns are allowed
        strict = False, 
        # Types will automatically be recast, if natural
        coerce = True  
    )

# a struct for storing x-pected standings for a given [league, season] league-style competition
# A Expected_Table must have:
    # Team MP, xPts, xGD
    # Can have any additional columns, as desired
class Expected_Table(Table):
    # Pandera schema defining league tabble daf
    Table_Schema = pa.DataFrameSchema(
        columns = {
            "Team": pa.Column(object),
            "MP":   pa.Column(int, pa.Check.ge(0)), # MP must be >= 0
            "xPts":  pa.Column(float, pa.Check.ge(0)), # Pts must be >= 0
            "xGD":   pa.Column(float),
        },
        # Additional columns are allowed
        strict = False, 
        # Types will automatically be recast, if natural
        coerce = True  
    )

# a struct for storing simulated standings for a given [league, season] league-style competition
# A Simulated_Tabled must have:
    # Team, MP, Simulated Pts, Simulated GD
    # Can have any additoinal columns, as desired
class Simulated_Table(Table):
    # Pandera schema defining league tabble daf
    Table_Schema = pa.DataFrameSchema(
        columns = {
            "Team": pa.Column(object),
            "MP":   pa.Column(int, pa.Check.ge(0)), # MP must be >= 0
            "Simulated Pts":  pa.Column(int, pa.Check.ge(0)), # Pts must be >= 0
            "Simulated GD":   pa.Column(int),
        },
        # Additional columns are allowed
        strict = False, 
        # Types will automatically be recast, if natural
        coerce = True  
    )

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