# for implementing a folder of operations
import goose.registry as registry
import typer

# imports necessary to run forecast
from goose.data.goose_data_structures.game_storage import Game, Game_Prediction, Games
from goose.data.built_in_data_types.schedule_data import schedule_data
from goose.operation.built_in_operations.utilities import load_model
from goose.data.goose_data_structures.identifiers import Team, League, Season
from goose.model import Model
import pandas as pd
from pathlib import Path

# subfolder of goose operations for prediction operations
# goose predict ...
prediction_operations = registry.goose_operations.create_subfolder("predict", description = "run a prediction")

# operation for predicting a game
# goose predict game [league] [home_team] [away_team] [model] Flag[--save]
@prediction_operations.operation("game", description = "predict a game")
def predict_game(league : League, home : Team, away : Team, model : Model):
        # Predict game
        typer.echo(f"Producing prediction of {home}(H) vs. {away}(A) via {model.model_name}...")
        game_prediction = model.Predict_Game(Game(home, away, None))
        # return game_prediction
        return game_prediction
# goose predict game [home_team] [away_team] [model] Flag[--save]
@predict_game.cli
def predict_game_cli(league : str, home : str, away : str, model_name : str, save: str = typer.Option(None, "--save", flag_value= ".", help ="Save to specified path")):
    # convert league + teams
    league = League(league)
    home = Team(home)
    away = Team(away)
    # load desired model
    model, model_name = load_model(model_name)
    # produce game_prediction
    game_prediction : Game_Prediction = predict_game(league, home, away, model)
    # Display game prediction to terminal
    game_prediction.view()
    # save game prediction, if requested
    if save:
        game_prediction.save(save)
        typer.echo(f"Saved to {save}")

# operation for predicting all remaining games in a leauge's seasons
@prediction_operations.operation("remaining-games", description = "predict all remaining games of a given league")
def predict_remaining(league : League, season : Season, model : Model):        
        # pull schedule of games to predict
        remaining_games = schedule_data.Retrieve(league, season, True)
        # Predict all remaining games
        typer.echo(f"Predicting all remaining {league.league} games via {model.model_name}...")
        game_predictions = Games[Game_Prediction](None)
        for game in remaining_games.games:
              game_predictions.Add_Game(model.Predict_Game(game))
        # return game_predictions
        return game_predictions
# goose predict remaining-games [league] [season] [model] Flag[--save]
@predict_remaining.cli
def predict_remaining_cli(league : str, season : int, model_name : str, save: str = typer.Option(None, "--save", flag_value= ".", help ="Save to specified path")):
    # convert league + season
    league = League(league)
    season = Season(season)
    # load desired model
    model, model_name = load_model(model_name)
    # produce remaining game predictions
    game_predictions : Games = predict_remaining(league, season, model)
    # Display game prediction to terminal
    print(game_predictions)
    # save game prediction, if requested
    if save:
        game_predictions.save_data(Path(save))
        typer.echo(f"Saved to {save}")

