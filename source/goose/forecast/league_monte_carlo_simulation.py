# for data handling
import pandas as pd
from goose.data.goose_data_structures import Game, Games, League_Table

# for implementing a monte carlo simulation forecast
from goose.forecast.monte_carlo_simulation import Monte_Carlo_Simulation
from goose.model import Model
from abc import ABC, abstractmethod

# abstract class for running a league (i.e. round-robin style, no KO) competition monte-carlo simulation
# Determines the simulated frequency probability of outcomes of each team:
    # winning league
    # securing CL, EL, UECL / equivalents
    # being relegated
    # etc...
# league competition monte-carlo depends on the placement significances of the specific league
    # this is specified by unique concrete subclasses for each league
class League_Monte_Carlo_Simulation(Monte_Carlo_Simulation, ABC):
    # Initialized as a forecast with parameter num_simulations
    def __init__(self, forecast_name, model : Model, games : Games, num_simulations, existing_standings : League_Table = None):
        super().__init__(forecast_name, model, games, num_simulations, existing_standings)
        # for league monte-carlo simulation, all simulations will produce League_Table
        self.simulations : list[League_Table] = []

    # conrete competition-specific knowledge of placement significances must be supplied
        # i.e. in PL, places 1-5 get CL; 18-20 get relegated, etc.
    @property
    @abstractmethod
    def placement_significances(self):
        pass

    # simulator for league-style competition (i.e. round robin, not KO)
    def run_simulation(self):
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
        # Summarize simulated results in a dataframe
        simulated_results = League_Table(pd.DataFrame.from_dict(simulated_results, orient = "index").rename_axis("Team").reset_index(drop = False))
        # sort by poilnts, goal_diff
        simulated_results.standings = simulated_results.standings.sort_values(by = ["Pts", "GD"], ascending=False)
        # if existing standings provided, combine existing and simulated results to get simulated final standings
        if self.existing_standings != None:
            simulated_results = self.Compute_Final_Standings(simulated_results)
        # store simulation
        self.simulations.append(simulated_results)

    # Randomly simulates a result for specified game according to model
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
    
    # Computes final standings combining existing_standings and simulated results
    def Compute_Final_Standings(self, simulated_results : League_Table):
        # Simplify existing standings (only basic data needed)
        self.existing_standings.simplify()
        # combine existing_standings and predicted_results (on team name)
        # merge on Team, applying suffixes _existing and _predicting
        simulated_standings = pd.merge(self.existing_standings.standings, simulated_results.standings, on = "Team", suffixes=('_existing', '_predicted'))
        # compute combined stats
        simulated_standings["MP"] = simulated_standings["MP_existing"] + simulated_standings["MP_predicted"]
        simulated_standings["Pts"] = simulated_standings["Pts_existing"] + simulated_standings["Pts_predicted"]
        simulated_standings["GD"] = simulated_standings["GD_existing"] + simulated_standings["GD_predicted"]
        # Keep only combined columns
        simulated_standings = League_Table(simulated_standings)
        simulated_standings.standings = simulated_standings.standings[["Team", "MP", "Pts", "GD"]]
        # Rename columns
        simulated_standings.standings.rename(columns = {"Pts" : "Simulated Pts", "GD" : "Simulated GD"})
        # sort by (Pts, GD)
        simulated_standings.standings = simulated_standings.standings.sort_values(by = ["Pts", "GD"], ascending = False)
        # return simulated_standings
        return simulated_standings

    # Interprets monte carlo simulation in context of a league-based competition
    def interpret(self):
        # extract teams involved in simulations
        teams = self.simulations[0].standings["Team"].unique()
        # tally occurences of each placement
        result_occurences = { # all categories to consider, as specific by the league's placement_significances
            team: {**{"Avg Position": 0}, **{label : 0 for label in self.placement_significances}} 
            for team in teams
        }
        for sim in self.simulations:
            sim = sim.standings.reset_index(drop = True)
            # consider eadh team
            for index, row in sim.iterrows():
                team = row["Team"]
                position = index + 1 # index = 0-based; league position is 1-based
                # Tally placement occurences
                result_occurences[team]["Avg Position"] += position
                # all league specific placement categories
                for category, (low, high) in self.placement_significances.items():
                    if low <= position <= high:
                        result_occurences[team][category] += 1
        # Convert dictionary to a pandas dataframe
        result_occurences = pd.DataFrame.from_dict(result_occurences, orient = "index").rename_axis("Team").reset_index(drop = False)
        # Convert occurence results to %
        results = result_occurences.copy()
        numeric_columns = results.columns.drop("Team")
        results[numeric_columns] = results[numeric_columns] / self.num_simulations
        # sort by [avg. position]
        results = results.sort_values(by = "Avg Position")
        self.interpretation = results
    
    # save interpretation
    def save_interpretation(self, path):
        self.interpretation.to_csv(path)

    # view interpretation
    def view_interpretation(self):
        print(self.interpretation.head(20))

# class for running a PL monte-carlos simulation 
# Determines the frequency probability via simulation of each team:
    # winning league
    # securing CL
    # securing EL
    # securing UECL
    # being relegated
class PL_Monte_Carlo_Simulation(League_Monte_Carlo_Simulation):
    # knowledge of the PL's placement significances
        # i.e. places 1-5 get CL; 18-20 get relegated, etc.
    placement_significances = {
            "Title" : (1, 1),
            "CL" : (1, 5),
            "EL" : (6, 6),
            "UECL" : (7, 7),
            "Relegation" : (18, 20)
        }

# class for running a Bundesliga monte-carlos simulation 
# Determines the frequency probability via simulation of each team:
    # winning league
    # securing CL
    # securing EL
    # securing UECL
    # being relegated
class Bundesliga_Monte_Carlo_Simulation(League_Monte_Carlo_Simulation):
    # knowledge of the Bundesliga's placement significances
        # i.e. places 1-5 get CL; 18-20 get relegated, etc.
    placement_significances = {
            "Title" : (1, 1),
            "CL" : (1, 4),
            "EL" : (5, 5),
            "UECL" : (6, 6),
            "Relegation" : (17, 18)
        }

# class for running a Laliga monte-carlos simulation 
# Determines the frequency probability via simulation of each team:
    # winning league
    # securing CL
    # securing EL
    # securing UECL
    # being relegated
class Laliga_Monte_Carlo_Simulation(League_Monte_Carlo_Simulation):
    # knowledge of Laliga's placement significances
        # i.e. places 1-5 get CL; 18-20 get relegated, etc.
    placement_significances = {
            "Title" : (1, 1),
            "CL" : (1, 4),
            "EL" : (5, 5),
            "UECL" : (6, 6),
            "Relegation" : (18, 20)
        }

# class for running a Ligue 1 monte-carlos simulation 
# Determines the frequency probability via simulation of each team:
    # winning league
    # securing CL
    # securing EL
    # securing UECL
    # being relegated
class Ligue1_Monte_Carlo_Simulation(League_Monte_Carlo_Simulation):
    # knowledge of the Ligue1's placement significances
        # i.e. places 1-5 get CL; 18-20 get relegated, etc.
    placement_significances = {
            "Title" : (1, 1),
            "CL" : (1, 4),
            "EL" : (5, 5),
            "UECL" : (6, 6),
            "Relegation" : (17, 18)
        }

# class for running a Serie A monte-carlos simulation 
# Determines the frequency probability via simulation of each team:
    # winning league
    # securing CL
    # securing EL
    # securing UECL
    # being relegated
class SerieA_Monte_Carlo_Simulation(League_Monte_Carlo_Simulation):
    # knowledge of the SerieA's placement significances
        # i.e. places 1-5 get CL; 18-20 get relegated, etc.
    placement_significances = {
            "Title" : (1, 1),
            "CL" : (1, 4),
            "EL" : (5, 5),
            "UECL" : (6, 6),
            "Relegation" : (18, 20)
        }