# for implementing a folder of operations
import goose.registry as registry
import typer
from typing import Annotated

# imports necessary to run forecast
from goose.operation.built_in_operations.utilities import load_model, league_MC_mappings
from goose.data.built_in_data_types.schedule_data import schedule_data
from goose.data.built_in_data_types.standings_data import standings_data
from goose.name_standardization import standardize_league_name
from goose.forecast.league_expectation import League_Expectation
from goose.forecast.monte_carlo_simulation import Monte_Carlo_Simulation

# subfolder of goose operations for forecast operations
# goose folder ...
forecast_operations = registry.goose_operations.create_subfolder("forecast", description = "run a forecast")

# operation for running an expectation
# goose forecast expectation [league] [model] Flag[--save]
@forecast_operations.operation("expectation", description = "run an expectation")
def expectation(league : str, 
                model_name : str, 
                save: str = typer.Option(None, "--save", flag_value= ".", help ="Save to specified path")):
    """Expectation forecast a league"""
    league = standardize_league_name(league)
    # load desired model
    model, model_name = load_model(model_name)
    # Retrieve league-specific data   
    typer.echo(f"Retrieving latest {league} data...")
    league_schedule = schedule_data.Retrieve(league, "2025-2026", True)
    league_standings = standings_data.Retrieve(league, "2025-2026")
    # run forecast
    typer.echo(f"Running expectation for {league} using {model_name}")
    forecast = League_Expectation(league + "_expectation", model, league_schedule, league_standings)
    forecast.Run_Forecast()
    # Display forecast to terminal
    forecast.View_Forecast()
    # save forecast, if requested
    if save:
        forecast.Save_Forecast(save)

# operation for running a monte-carlo simulation
# goose forecast monte-carlo [league] [model] Flag[--sims] Flag[--save]
@forecast_operations.operation("monte-carlo", description = "run an monte-carlo simulation")
def monte_carlo(league: str, 
                model_name : str, 
                num_sims : Annotated[int, typer.Option("--sims", "-n", help="Number of simulations to run")] = 10000,
                save: str = typer.Option(None, "--save", flag_value= ".", help ="Save to specified path")):
    """Monte-Carlo forecast a league"""
    league = standardize_league_name(league)
    # load desired model
    model, model_name = load_model(model_name)
    # Retrieve league-specific data    
    typer.echo(f"Retrieving latest {league} data...")
    league_schedule = schedule_data.Retrieve(league, "2025-2026", True)
    league_standings = standings_data.Retrieve(league, "2025-2026")
    # run forecast
    typer.echo(f"Running {num_sims} simulations for {league} using {model_name}...")
    forecast : Monte_Carlo_Simulation = None
    forecast = league_MC_mappings[league](league + "_monte-carlo-simulation", model, league_schedule, num_sims, league_standings)
    forecast.Run_Forecast()
    # Display forecast to terminal
    forecast.View_Forecast()
    # save forecast, if requested
    if save:
        forecast.Save_Forecast(save)