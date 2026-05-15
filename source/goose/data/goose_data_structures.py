# for defining data structures
import pandas as pd
import pandera.pandas as pa
from datetime import datetime
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Self
from collections import deque

# for displaying data
from rich.tree import Tree
from rich.console import Console

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

# a struct for storing / defining a tie of a knockout competition bracket
# all ties have:
    # team one and team two, defined recursively via ties
    # winning team - winner between team one and team two
    # (optionally) - name of the round this tie is
    # whether or not the tie has been completed
class Tie:
    # initialized with necessary info
    def __init__(self, team_one_source : Self | Team, team_two_source : Self | Team, round : str = "", winning_team : Team = None):
        self.team_one_source = team_one_source
        self.team_two_source = team_two_source
        self.winning_team = winning_team
        self.round = round
        self.completed : bool = True if winning_team else False
    
    # Returns team_one of this tie
    # team_one is naturally the .winning_team of team_one_source
    @property
    def team_one(self):
        # if team_one_source is already resolved
        if isinstance(self.team_one_source, Team):
            return self.team_one_source
        # otherwise, recursively resolve .winning_team of team_one_source
        else:
            return self.team_one_source.winning_team
        
    # Returns team_two of this tie
    # team_two is naturally the .winning_team of team_two_source
    @property
    def team_two(self):
        # if team_two_source is already resolved
        if isinstance(self.team_two_source, Team):
            return self.team_two_source
        # otherwise, recursively resolve .winning_team of team_two_source
        else:
            return self.team_two_source.winning_team
        
    # Retrieve the Games the tie consists of
    # If teams are not yet known, games are specified with unknown teams
    @abstractmethod
    def retrieve_games(self) -> Games:
        pass

    # Sets the winning team as specified team
    def set_winner(self, team : Team):
        self.winning_team = team
        # indicate that the tie has been completed
        self.completed = True

    # returns tie information stored as a dictionary
    @abstractmethod
    def to_dict(self):
        pass

    # saves the given tie to a file

# defines a single-legged, neutral venue tie (i.e. the CL final)
# for neutral venue, home team vs away team technically exists, but doesn't functionally matter
# home_team = team_one, away_team = team_two
class Single_Neutral_Match(Tie):
    # Retrieves the Game object associated with match
    def retrieve_games(self):
        return Games(Game(self.team_one, self.team_two, date = datetime.now(), neutral_venue = True))
    
    # returns tie information stored as a dictionary
    @abstractmethod
    def to_dict(self):
        return {
            "round" : self.round,
            "tie type" : self.__class__.__name__,
            "team one" : self.team_one,
            "team two" : self.team_two,
            "winning team" : self.winning_team,
            "completed" : self.completed
        }
    
# defines a two-legged, home and away tie (i.e. CL SF)
# team_home_first_leg = team_one, team_home_second_leg = team_two
class Two_Legged_Home_Away(Tie):
    # Initialized given which team is home/away in the second leg
    def __init__(self, team_home_second_leg_source : Self | Team, team_away_second_leg_source : Self | Team, round : str = "", winning_team : Team = None):
        super().__init__(team_home_second_leg_source, team_away_second_leg_source, round, winning_team)

    # Wrapper for accessing team_home_second_leg
    @property
    def team_home_second_leg(self):
        return self.team_one
    
    # Wrapper for accessign team_away_second_leg
    @property
    def team_away_second_leg(self):
        return self.team_two

    # Retrieves the Game objects associated with the 2 legs
    def retrieve_games(self):
        # leg 1
        leg_1 = Game(self.team_away_second_leg, self.team_home_second_leg, datetime.now())
        # leg 2
        leg_2 = Game(self.team_home_second_leg, self.team_away_second_leg, datetime.now())
        # returns both legs as Games object
        return Games([leg_1, leg_2])
    
    # returns tie information stored as a dictionary
    @abstractmethod
    def to_dict(self):
        return {
            "round" : self.round,
            "tie type" : self.__class__.__name__,
            "team home second leg" : self.team_home_second_leg,
            "team away second leg" : self.team_away_second_leg,
            "winning team" : self.winning_team,
            "completed" : self.completed
        }
    
# struct for storing a bracket
# Includes:
    # root_tie = the final rooting the bracket
    # (optinally) the league and season of the competition
    # .teams_invovled storing a list of all teams involved in the bracket
class Bracket:
    def __init__(self, root_tie : Tie, league : League = None, season : str = None):
        self.root_tie = root_tie
        self.league = league
        self.season = season
        # retrieve list of all teams involved in the bracket
        self.teams_involved : set = self.retrieve_teams_involved(self.root_tie)

    # retrieves all teams recursively down from specified tie
    @staticmethod
    def retrieve_teams_involved(root : Tie | Team) -> list[Team]:
        teams_involved = set()
        # if root is a team
        if isinstance(root, Team):
            teams_involved.add(root)
        # otherwise, recurse on both branches
        else:
            teams_involved.update(Bracket.retrieve_teams_involved(root.team_one_source))
            teams_involved.update(Bracket.retrieve_teams_involved(root.team_two_source))
        # return the list of teams
        return teams_involved
    
    # retrieves the next "deepest" tie yet to have been completed = specified a winner
    # effectively, depth first searches to discover deepest tie with .completed == False
    def retrieve_next_tie(self) -> Tie | None:
        if not self.root_tie or self.root_tie.completed:
            # If the Final is done, the whole tournament is done
            if self.root_tie and self.root_tie.completed:
                return None
            return self.root_tie
        # Queue for level-order traversal (BFS)
        queue = deque([self.root_tie])
        uncompleted_ties = []
        while queue:
            current = queue.popleft()
            if isinstance(current, Tie):
                if not current.completed:
                    uncompleted_ties.append(current)
                # Add children to the queue to keep searching deeper
                queue.append(current.team_two_source)
                queue.append(current.team_one_source)
        if not uncompleted_ties:
            return None
        # Because BFS finds the Root (Final) first and the QFs last,
        # the 'deepest' ties are at the END of our uncompleted list.
        return uncompleted_ties[-1]
    
    # builds rich tree object for displaying bracket tree
    def retrieve_display_tree(self):
        title = f"[bold magenta]{self.league} {self.season} Bracket[/]"
        display_tree = Tree(title, guide_style="bright_black")
        self.build_display_tree(self.root_tie, display_tree)
        return display_tree

    # helper to build display tree from deeper >= root
    @staticmethod
    def build_display_tree(root : Tie | Team, tree_branch : Tree):
        # if root is a team, display it
        if isinstance(root, Team):
            tree_branch.add(f"[green]{root}[/]")
            return
        # otherwise, display tie's info
        winner = f"([yellow]{root.winning_team}[/])" if root.completed else ""
        tie_info = f"[dim]({root.__class__.__name__})[/]"
        label = f"[bold white]{root.round}[/] {winner} {tie_info}"
        # create rich tree object for this tie
        current_tie = tree_branch.add(label)
        # Recursively build rich tree for both branches
        Bracket.build_display_tree(root.team_one_source, current_tie)
        Bracket.build_display_tree(root.team_two_source, current_tie)

    # view bracket in terminal
    def view_bracket(self):
        bracket_tree = self.retrieve_display_tree()
        Console().print("\n", bracket_tree, "\n")

    # save bracket to specified file
    def save_bracket(self, file_path):
        bracket_tree = self.retrieve_display_tree()
        with open(file_path, "w", encoding="utf-8") as f:
            file_console = Console(file=f, force_terminal=False, width=120)
            file_console.print(bracket_tree)

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