# for defining data structures
from datetime import datetime
from abc import abstractmethod
from collections import deque
from typing import Self
from goose.data.goose_data_structures.identifiers import Team, League, Season
from goose.data.goose_data_structures.game_storage import Game, Games

# for invoking models
from goose.model import Model

# for performing game expectations
from goose.forecast.expectation import Expectation

# for displaying data in tree-structure
from rich.tree import Tree
from rich.console import Console

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

    # Sets the winning team as specified team
    def set_winner(self, team : Team):
        self.winning_team = team
        # indicate that the tie has been completed
        self.completed = True

    # Performs expectation of the tie
    # returns (team_1_xg, team_2_xg)
    def expect(self : Self, model : Model) -> tuple[float, float]:
        pass

    # returns tie information stored as a dictionary
    @abstractmethod
    def to_dict(self):
        pass

# defines a single-legged, neutral venue tie (i.e. the CL final)
# for neutral venue, home team vs away team technically exists, but doesn't functionally matter
# home_team = team_one, away_team = team_two
class Single_Neutral_Match(Tie):
    # Retrieves the Game object associated with match
    def retrieve_games(self):
        return Game(self.team_one, self.team_two, date = datetime.now(), neutral_venue = True)
    
    # Performs expectation of the tie
    def expect(self : Self, model : Model) -> tuple[float, float]:
        # retrieve the associated game
        game : Game = self.retrieve_games()
        # expect the game
        team_1_xg, team_2_xg, _, _ = Expectation.Expect_Game(game, model)
        # return expectation
        return team_1_xg, team_2_xg

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
# team_home_second_leg = team_one, team_away_second_leg = team_two
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
    
    # Performs expectation of the tie
    def expect(self : Self, model : Model) -> tuple[float, float]:
        # retrieve the associated games
        games : Games = self.retrieve_games()
        leg_1 = games[0]
        leg_2 = games[1]
        # expect leg 1
        team_2_xg_leg1, team_1_xg_leg1, _, _ = Expectation.Expect_Game(leg_1, model)
        # expect leg 2
        team_1_xg_leg2, team_2_xg_leg2, _, _ = Expectation.Expect_Game(leg_2, model)
        # combine two legs
        team_1_xg = team_1_xg_leg1 + team_1_xg_leg2
        team_2_xg = team_2_xg_leg1 + team_2_xg_leg2
        # return expectation
        return team_1_xg, team_2_xg
    
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
    def __init__(self, root_tie : Tie, league : League = None, season : Season = None):
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