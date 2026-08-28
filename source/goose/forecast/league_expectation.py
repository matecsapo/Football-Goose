# for data manipulation
import pandas as pd
from goose.data.goose_data_structures.game_storage import Game_Points_Expectation, Games
from goose.data.goose_data_structures.standings_storage import League_Table, Expected_Table
from pathlib import Path
import os

# for implementing a forecast
from goose.forecast.expectation import Expectation

# for employing a model
from goose.model import Model

# class for expecting out results of a set of games
class League_Expectation(Expectation):
    # PL_Expext_Forecast requires no special parameters
    def __init__(self, forecast_name : str, model : Model, games : Games, existing_standings : League_Table = None):
        super().__init__(forecast_name, model)
        self.games = games
        self.existing_standings = existing_standings
        # league expecation forecast consist of (expected results, expected final standings)
        # for storing expected results
        self.expected_results = None
        # for storing expected final standings
        self.expected_standings : Expected_Table = None

    # Performs full forecast:
        # expects out set of games
        # Computes final standings combination of existing_standings and predicted results
    def Run_Forecast(self):
        # Expect out the set of games
        self.Expect_Games()
        # if existing standings provided, computes final standings
        if self.existing_standings != None:
            self.Compute_Final_Standings()
        # store forecast
        self.forecast = (self.expected_results, self.expected_standings)

    # Returns combined expected results over all games
    def Expect_Games(self):
        # Determine all teams involved in games
        teams = set()
        for game in self.games.games:
            teams.add(game.home_team)
            teams.add(game.away_team)
        # Expect out all games
        expected_results = {team: {"MP" : 0,"Pts" : 0} for team in teams}
        for game in self.games.games:
            # Get expectation of game
            game_points_expectation : Game_Points_Expectation = self.Expect_Game(game, self.model)
            # Update MP of each team
            expected_results[game.home_team]["MP"] += 1
            expected_results[game.away_team]["MP"] += 1
            # update points of each team
            expected_results[game.home_team]["Pts"] += game_points_expectation.home_xPts
            expected_results[game.away_team]["Pts"] += game_points_expectation.away_xPts
        # Summarize expected_results in a dataframe
        expected_results = pd.DataFrame.from_dict(expected_results, orient = "index").rename_axis("Team").reset_index(drop = False)
        expected_results = expected_results.sort_values("Pts", ascending=False)
        # return expected_results
        self.expected_results = expected_results

        # Computes final standings combining existing_standings and predicted results
    def Compute_Final_Standings(self):
        # Simplify existing standings (only basic data needed)
        self.existing_standings.simplify()
        # combine existing_standings and predicted_results (on team name)
        # merge on Team, applying suffixes _existing and _predicting
        self.expected_standings = pd.merge(self.existing_standings.standings, self.expected_results, on = "Team", suffixes=('_existing', '_predicted'))
        # compute combined stats
        self.expected_standings["MP"] = self.expected_standings["MP_existing"] + self.expected_standings["MP_predicted"]
        self.expected_standings["xPts"] = self.expected_standings["Pts_existing"] + self.expected_standings["Pts_predicted"]
        # store into Expected_Table
        self.expected_standings = Expected_Table(self.expected_standings)
        # Keep only basic created columns
        self.expected_standings.simplify()
        # sort by (Pts, GD)
        self.expected_standings.standings = self.expected_standings.standings.sort_values("xPts", ascending = False)
    
    # displays forecast to terminal:
        # displays expected results
        # displays expected standings
    def View_Forecast(self):
        # expected results
        print("Expected Results")
        print(self.expected_results)
        # expected standings
        print("")
        print("Expected Standings")
        self.expected_standings.view()

    # saves forecast to folder directory/self.forecast
        # saves expected results
        # saves expected standings
    def Save_Forecast(self, directory : str):
        folder = Path(directory) / self.forecast_name
        os.makedirs(folder, exist_ok=True)
        # expected results
        self.expected_results.to_csv(folder / "expected_results.csv")
        # expected standings
        self.expected_standings.save(folder / "expected_standings.csv")
