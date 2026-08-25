# for manipulating data
from pathlib import Path
from goose.data.goose_data_structures.identifiers import Team
from goose.data.goose_data_structures.bracket_storage import Tie, Bracket
from goose.forecast.expectation import Expectation
from copy import deepcopy
from random import choice

# for implementing a forecast
from goose.forecast.expectation import Expectation
from abc import abstractmethod

# for employing a model
from goose.model import Model

# class for performing a bracket expectation
class Bracket_Expectation(Expectation):
    # Bracket_Expectation takes in the bracket to expect out to
    def __init__(self, forecast_name : str, model : Model, bracket : Bracket):
        super().__init__(forecast_name, model)
        # for storing the initial bracket
        self.bracket = bracket
        # for storing the expect bracket
        self.expected_bracket : Bracket = None
        # bracket expectation self.forecast consists of self.expected_bracket

    # Performs complete expectation forecast of the bracket
    def Run_Forecast(self):
        # start expectation at inputted state of bracket
        self.expected_bracket = deepcopy(self.bracket)
        # Expect out ties in order of depth until final
        while True:
            next_tie = self.expected_bracket.retrieve_next_tie()
            # if no ties left, break
            if next_tie is None:
                break
            # Expect out the tie
            expected_winner = self.Expect_Tie(next_tie)
            next_tie.set_winner(expected_winner)
        # store forecast
        self.forecast = self.expected_bracket
    
    # Expects out given tie, returning the winning team
    @staticmethod
    def Expect_Tie(tie : Tie, model : Model) -> Team:
        # expect out the tie
        team_1_xg, team_2_xg = tie.expect(model)
        # if expects a draw, random pick a team
        if team_1_xg == team_2_xg:
            return choice([tie.team_one, tie.team_two])
        # otherwise, return expected winner
        elif team_1_xg > team_2_xg:
            return tie.team_one
        else:
            return tie.team_two
        
    # prints expected bracket to terminal
    def View_Forecast(self):
        self.expected_bracket.view_bracket()

    # saves expected bracket to folder directory/self.forecast_expected_bracket
    @abstractmethod
    def Save_Forecast(self, directory : str):
        path = Path(directory) / f"{self.forecast_name}_expected_bracket"
        self.expected_bracket.save_bracket(path)

