# for implementing a folder of operations
import goose.registry as registry
import typer
from typing import Annotated

# imports necessary to run forecast
from goose.operation.built_in_operations.utilities import load_model, league_MC_mappings
from goose.data.built_in_data_types.schedule_data import schedule_data
from goose.data.built_in_data_types.standings_data import standings_data
from goose.data.goose_data_structures.identifiers import League, Season
from goose.forecast.league_expectation import League_Expectation
from goose.forecast.monte_carlo_simulation import Monte_Carlo_Simulation
from goose.model import Model

# subfolder of goose operations for forecast operations
# goose folder ...
forecast_operations = registry.goose_operations.create_subfolder("forecast", description = "run a forecast")

# operation for running an expectation
@forecast_operations.operation("expectation", description = "run an expectation")
def expectation(league : League, season : Season, model : Model):
    # Retrieve league-specific data   
    league_schedule = schedule_data.Retrieve(league, season, True)
    league_standings = standings_data.Retrieve(league, season)
    # run forecast
    typer.echo(f"Producing {league.league} expectation via {model.model_name}...")
    forecast = League_Expectation(league.league + "_expectation", model, league_schedule, league_standings)
    forecast.Run_Forecast()
    # return forecast
    return forecast
# goose forecast expectation [league] [season] [model] Flag[--save]
@expectation.cli
def expectation_cli(league : str, season : int, model_name : str, save: str = typer.Option(None, "--save", flag_value= ".", help ="Save to specified path")):
    # convert league + season
    league = League(league)
    season = Season(season)
    # load desired model
    model, model_name = load_model(model_name)
    # produce forecast
    forecast : League_Expectation = expectation(league, season, model)
    # Display forecast to terminal
    forecast.View_Forecast()
    # save forecast, if requested
    if save:
        forecast.Save_Forecast(save)
        typer.echo(f"Saved to {save}")

# operation for running a monte-carlo simulation
@forecast_operations.operation("monte-carlo", description = "run an monte-carlo simulation")
def monte_carlo(league : League, season : Season, model : Model, num_sims : int = 10000): 
    league_schedule = schedule_data.Retrieve(league, season, True)
    league_standings = standings_data.Retrieve(league, season)
    forecast : Monte_Carlo_Simulation = None
    forecast = league_MC_mappings[league](league.league + "_monte-carlo-simulation", model, league_schedule, num_sims, league_standings)
    typer.echo(f"Producing {league.league} Monte-Carlo ({num_sims} simulations) via {model.model_name}...")
    forecast.Run_Forecast()
    # return forecast
    return forecast
# goose forecast monte-carlo [league] [season] [model] Flag[--sims] Flag[--save]
@monte_carlo.cli
def monte_carlo_cli(league : str, season : int, model_name : str, num_sims : Annotated[int, typer.Option("--sims", "-n", help="Number of simulations to run")] = 10000,
                save: str = typer.Option(None, "--save", flag_value= ".", help ="Save to specified path")):
    # convert league + season
    league = League(league)
    season = Season(season)
    # load desired model
    model, model_name = load_model(model_name)
    # produce forecast
    forecast : Monte_Carlo_Simulation = monte_carlo(league, season, model, num_sims)
    # Display forecast to terminal
    forecast.View_Forecast()
    # save forecast, if requested
    if save:
        forecast.Save_Forecast(save)
        typer.echo(f"Saved to {save}")