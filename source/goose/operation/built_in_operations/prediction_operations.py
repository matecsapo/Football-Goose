# for implementing a folder of operations
import goose.registry as registry
import typer

# imports necessary to run forecast
from goose.data.goose_data_structures import Game
from goose.data.built_in_data_types.schedule_data import schedule_data
from goose.operation.built_in_operations.utilities import load_model
from goose.data.goose_data_structures import Team, League
import pandas as pd
from pathlib import Path

# subfolder of goose operations for prediction operations
# goose predict ...
prediction_operations =  registry.goose_operations.create_subfolder("predict", description = "run a prediction")

# operation for predicting a game
# goose predict game [league] [home_team] [away_team] [model] Flag[--save]
@prediction_operations.operation("game", description = "predict a game")
def predict_game(league : str, 
                 home: str, 
                 away: str, 
                 model_name : str, 
                 save: str = typer.Option(None, "--save", flag_value= ".", help ="Save to specified path")):
        """Predict a single game"""
        if isinstance(league, str):
            league = League(league)
        # Standardize team names
        if isinstance(home, str):
            home = Team(home)
        if isinstance(away, str):
            away = Team(away)
        # load desired model
        model, model_name = load_model(model_name)
        # Predict game
        typer.echo(f"{model_name}Predicting {home.team}(h) vs. {away.team}(a)")
        game_prediction = model.Predict_Game(Game(home, away, None))
        # Display game prediction to terminal
        game_prediction.view()
        # save game prediction, if requested
        if save:
            game_prediction.save(save)

# operation for predicting all remaining games in a leauge's seasons
# goose predict remaining-games [league] [model]
@prediction_operations.operation("remaining-games", description = "predict all remaining games of a given league")
def predict_remaining(league : str, 
                 model_name : str, 
                 save: str = typer.Option(None, "--save", flag_value= ".", help ="Save to specified path")):
        """Predict a single game"""
        if isinstance(league, str):
            league = League(league)
        # load desired model
        model, model_name = load_model(model_name)
        # pull schedule of games to predict
        typer.echo(f"Predicting all remaining {league.league} games...")
        remaining_games = schedule_data.Retrieve(league, "2025-2026", True)
        # Predict all remaining games
        game_predictions = []
        for game in remaining_games.games:
              game_predictions.append(model.Predict_Game(game).to_dict())
        # convert to dataframe
        game_predictions = pd.DataFrame(game_predictions)
        # Display game prediction to terminal
        print(game_predictions)
        # save game prediction, if requested
        if save:
            game_predictions.to_csv(Path(save) / f"{league}_game_predictions.csv")