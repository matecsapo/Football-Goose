from abc import ABC, abstractmethod

# for data manipulation
import json
import pandas as pd
from goose.engine.data import Game, Games, Game_Prediction, Standings_Data, Schedule_Data

# for implementing a forecast
from goose.engine.forecast import Forecast

# for employing a model
from goose.engine.model import Model

# for implementing a PL monte-carlo simulator
from goose.engine.monte_carlo import Monte_Carlo_Simulation

# abstract class for predicting results of a set of games
class League_Forecast(Forecast, ABC):
    # Computes final standings combining existing_standings and predicted results
    def Compute_Final_Standings(self):
        # Simplify existing standings (only basic data needed)
        self.existing_standings.Simplify()
        # combine existing_standings and predicted_results (on team name)
        # merge on Team, applying suffixes _existing and _predicting
        self.predicted_standings = pd.merge(self.existing_standings.data, self.predicted_results, on = "Team", suffixes=('_existing', '_predicted'))
        # compute combined stats
        self.predicted_standings["MP"] = self.predicted_standings["MP_existing"] + self.predicted_standings["MP_predicted"]
        self.predicted_standings["Pts"] = self.predicted_standings["Pts_existing"] + self.predicted_standings["Pts_predicted"]
        self.predicted_standings["GD"] = self.predicted_standings["GD_existing"] + self.predicted_standings["GD_predicted"]
        # Keep only combined columns
        self.predicted_standings = self.predicted_standings[["Team", "MP", "Pts", "GD"]]
        # sort by (Pts, GD)
        self.predicted_standings = self.predicted_standings.sort_values(by = ["Pts", "GD"], ascending = False)
    
    # Display predicted results:
        # To temp file
        # To terminal
    def View_Predicted_Results(self):
        self.predicted_results.to_csv("predicted_results.csv")
        print(self.predicted_results)

    # Display predicted standings:
        # To temp file
        # To terminal
    def View_Predicted_Standings(self):
        self.predicted_standings.to_csv("predicted_standings.csv")
        print(self.predicted_standings)

# class for expecting out results of a set of games
class League_Expect_Forecast(League_Forecast):
    # PL_Expext_Forecast requires no additional fields
    def __init__(self, model : Model, games : Games, existing_standings : Standings_Data = None):
        super().__init__(model, games, existing_standings)

    # Performs full forecast:
        # expects out set of games
        # Computes final standings combination of existing_standings and predicted results
    def Forecast(self):
        # Expect out the set of games
        self.Expect_Games()
        # Compute final standings
        self.Compute_Final_Standings()

    # Returns expected value of goals scored + points achieved by each team in specified game
    def Expect_Game(self, game : Game):
        prediction = self.model.Predict_Game(game)
        # determine xp of both teams
        home_xp = 0 * prediction.prob_away_win + 1 * prediction.prob_draw + 3 * prediction.prob_home_win
        away_xp = 0 * prediction.prob_home_win + 1 * prediction.prob_draw + 3 * prediction.prob_away_win
        # return xg and xp of both teams
        return prediction.home_xg, prediction.away_xg, home_xp, away_xp
    
    # Returns combined expected results over all games
    def Expect_Games(self):
        # Determine all teams involved in games
        teams = set()
        for game in self.games.games:
            teams.add(game.home_team)
            teams.add(game.away_team)
        # Expect out all games
        expected_results = {team: {"MP" : 0,"Pts" : 0, "GD" : 0} for team in teams}
        for game in self.games.games:
            # Get expectation of game
            home_xg, away_xg, home_xp, away_xp = self.Expect_Game(game)
            # Update MP of each team
            expected_results[game.home_team]["MP"] += 1
            expected_results[game.away_team]["MP"] += 1
            # update points of each team
            expected_results[game.home_team]["Pts"] += home_xp
            expected_results[game.away_team]["Pts"] += away_xp
            # update goal_diff for both teams
            expected_results[game.home_team]["GD"] += home_xg - away_xg
            expected_results[game.away_team]["GD"] += away_xg - home_xg
        # Summarize expected_results in a dataframe
        expected_results = pd.DataFrame.from_dict(expected_results, orient = "index").rename_axis("Team").reset_index(drop = False)
        # sort by poilnts, goal_diff
        expected_results = expected_results.sort_values(by = ["Pts", "GD"], ascending=False)
        # return expected_results
        self.predicted_results = expected_results
    
#class for simulating out results of a set of games
class League_Simulate_Forecast(League_Forecast):
    # PL_Expext_Forecast requires no additional fields
    def __init__(self, model : Model, games : Games, existing_standings : Standings_Data = None):
        super().__init__(model, games, existing_standings)
    
    # Performs full forecast:
        # simulates out set of games
        # Computes final standings combination of existing_standings and predicted results
    def Forecast(self):
        # Expect out the set of games
        self.Simulate_Games()
        # Compute final standings
        self.Compute_Final_Standings()
    
    # Randomly simulates a result for specified game according to model prediction
    def Simulate_Result(self, game : Game):
        # Simulate the game according to model's prediction
        home_goals, away_goals = self.model.Simulate_Game(game)
        # determine result
        result = "d" # draw
        if home_goals > away_goals:
            result = "h"
        elif away_goals > home_goals:
            result = "a"
        # return result
        return {"result" : result,
                "home_goals" : home_goals,
                "away_goals" : away_goals}
    
    # Returns combined simulated results over all games
    def Simulate_Games(self):
        # Determine all teams involved in games
        teams = set()
        for game in self.games.games:
            teams.add(game.home_team)
            teams.add(game.away_team)
        # simulate out all games
        simulated_results = {team: {"MP" : 0,"Pts" : 0, "GD" : 0} for team in teams}
        for game in self.games.games:
            # Get simulation of game
            result = self.Simulate_Result(game)
            # Update MP of each team
            simulated_results[game.home_team]["MP"] += 1
            simulated_results[game.away_team]["MP"] += 1
            # update points of each team
            if result["result"] == "h":
                simulated_results[game.home_team]["Pts"] += 3
            elif result["result"] == "a":
                simulated_results[game.away_team]["Pts"] += 3
            else:
                simulated_results[game.home_team]["Pts"] += 1
                simulated_results[game.away_team]["Pts"] += 1
            # update goal_diff for both teams
            simulated_results[game.home_team]["GD"] += result["home_goals"] - result["away_goals"]
            simulated_results[game.away_team]["GD"] += result["away_goals"] - result["home_goals"]
        # Summarize expected_results in a dataframe
        simulated_results = pd.DataFrame.from_dict(simulated_results, orient = "index").rename_axis("Team").reset_index(drop = False)
        # sort by poilnts, goal_diff
        simulated_results = simulated_results.sort_values(by = ["Pts", "GD"], ascending=False)
        # return expected_results
        self.predicted_results = simulated_results

# abstract class for running a league competition monte-carlo simulation
# Determines the frequency probability via simulation of each team:
    # winning league
    # securing CL
    # securing EL
    # securing UECL
    # being relegated
# league competition monte-carlo depends on the placement significances
class League_Monte_Carlo_Simulation(Monte_Carlo_Simulation, ABC):

    # specific competitions interpretation depends on the placement significans
    def __init__(self, forecast : Forecast, num_simulations):
        self.placement_significances = None
        super().__init__(forecast, num_simulations)

    # Interprets monte carlo simulation in context of PL
    def interpret(self):
        # extract teams involved in simulations
        teams = self.simulations[0]["Team"].unique()
        # tally occurences of each placement
        result_occurences = {team : {"Avg Position" : 0, "Title" : 0, "CL" : 0, "EL" : 0, "UECL" : 0, "Relegated" : 0} for team in teams}
        for sim in self.simulations:
            sim = sim.reset_index(drop = True)
            # consider eadh team
            for index, row in sim.iterrows():
                team = row["Team"]
                position = index + 1 # index = 0-based; league position is 1-based
                # Tally placement occurences
                result_occurences[team]["Avg Position"] += position
                # Title
                if position >= self.placement_significances["Title"][0] and position <= self.placement_significances["Title"][1]:
                    result_occurences[team]["Title"] += 1
                # CL
                if position >= self.placement_significances["CL"][0] and position <= self.placement_significances["CL"][1]:
                    result_occurences[team]["CL"] += 1
                # EL
                if position >= self.placement_significances["EL"][0] and position <= self.placement_significances["EL"][1]:
                    result_occurences[team]["EL"] += 1
                # UECL
                if position >= self.placement_significances["UECL"][0] and position <= self.placement_significances["UECL"][1]:
                    result_occurences[team]["UECL"] += 1
                # Relegation
                if position >= self.placement_significances["Relegation"][0] and position <= self.placement_significances["Relegation"][1]:
                    result_occurences[team]["Relegated"] += 1
        # Convert dictionary to a pandas dataframe
        result_occurences = pd.DataFrame.from_dict(result_occurences, orient = "index").rename_axis("Team").reset_index(drop = False)
        # Convert occurence results to %
        results = result_occurences.copy()
        numeric_columns = results.columns.drop("Team")
        results[numeric_columns] = results[numeric_columns] / self.num_simulation
        # sort by [avg. position]
        results = results.sort_values(by = "Avg Position")
        self.interpretation = results
    
    def view_interpretation(self):
        self.interpretation.to_csv("PL_monte_carlo_.csv")
        print(self.interpretation.head(20))

# class for running a PL monte-carlos simulation 
# Determines the frequency probability via simulation of each team:
    # winning league
    # securing CL
    # securing EL
    # securing UECL
    # being relegated
class PL_Monte_Carlo_Simulation(League_Monte_Carlo_Simulation):
    # Initialized with knowledge of the PL's placement significances
        # i.e. places 1-5 get CL; 18-20 get relegated, etc.
    def __init__(self, forecast : Forecast, num_simulations):
        super().__init__(forecast, num_simulations)
        self.placement_significances = {
            "Title" : (1, 1),
            "CL" : (1, 5),
            "EL" : (6, 6),
            "UECL" : (7, 7),
            "Relegation" : (18, 20)
        }