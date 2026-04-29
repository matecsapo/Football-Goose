# Football-G.O.O.S.E. 🪿

**Football/Soccer (G)eneralized f(O)recast m(O)dels (S)imulation (E)ngine.**

Football-Goose is a python-based engine for developing Football/Soccer forecast models. Goose allows for a "plug-model-and-play" approach around model development. The Goose environment provides built-in functionality for generating Monte-Carlo simulations, calculating expected value statistics, retrieving source/raw data, and building data/model/projection pipelines. Goose is designed to be highly extensible for ease of implementing custom functionalities.

### Installation and Getting Started:
Football-Goose is packaged as a pyproject. It can be installed via pip by running
```bash
pip install git+https://github.com/matecsapo/football-goose.git
```
in terminal. Check pyproject.toml for dependencies and other details. Read the rest of README.md, below, to familiarze oneself with the engine's functionalities and interface.

For an example of building in the Goose engine environment, it is strongly recommended to check out [Football-Honk](https://github.com/matecsapo/football-honk), my own football modelling and projections, built using Football-Goose.

### Interacting with Goose Engine
To allow for generalized interaction with the Goose engine, a few standardizations are required:
* For a model to be Goose-compatible it must be a subset of class Model from goose.model. Goose is built specifically for models that map : (Game) -> (Prediction of Game), i.e. "single-game-predictors", not "season-at-once-predictors"
  * Goose provides Model.save_model_fgm() for storing goose-compatible models to a common .fgm file (folder) format
  * Model.load_model_fgm() can then be used to load a .fgm file (folder)
* Core data types are standardized in goose.data.goose_data_structures. Notably,
  * Game type for storing games
  * Games type for storing a set of games (for example, a "schedule" of matches)
  * Standings type for storing active league table, simulated standings, etc.
  * Game_Prediction type for defining information a model returns when "projecting" a game

### Forecasts
In Goose, a forecast is a means/logic of invoking a model to produce multi-game / season-length projections. Currently, Goose supports the 2 main such forecast logics commonly used in football modelling:
* class Forecast, from goose.forecast.forecast defines the Abstract class standardazing forecast operations. Custom forecast logics can be implemented by defining a subclass of Forecast
* class League_Expectation(Forecast) from goose.forecast.league_expectation implements expected value forecasting (i.e xPts, xPos, xGD, etc.) for league-style competitions (i.e. round-robin, not KO)
* class Monte_Carlo_Simulation(Forecast) from goose.forecast.monte_carlo implements monte-carlo simulation (i.e. % chance of winning title, getting relegated, etc.)
* class League_Monte_Carlo_Simulation from goose.forecast.league_monte_carlo implements an abstract monte-carlo simulation for league-style competitions. Specific leagues are implemented via concrete subclass that thereby specifies the "placement significances". Currently, PL, Laliga, Bundesliga, Serie A, Ligue 1 are supported natively; further leagues can be added as desired

### Operations
In Goose, an operation is a function/process that interacts with the Goose Engine. Operations are stored within Operations_Folder objects. All operations also automatically generate a corresponding command within the Goose CLI (see below). Goose provides the following folders of operations built-in:
* discover operations; "goose discover ..." : see below
* forecast operations; "goose forecast ..." : operations for performing specific forecasts given league, model, etc. parameters
* prediction operations; "goose predict ..." : operations for performing specific predictions given league, model, etc. parameters

Usefully, custom operations can be defined as follows:
* a new operations folder can be created via ```python (superfolder).create_subfolder(subfolder_name, subfolder_descrition)```
* a new operation function definition can be added to an operation folder via decorator ```python @(folder).operation(operation_name, operation_description)```
* As with the built-in operations, custom operations automatically generate a corresponding command accessible in Goose CLI (see below)

### Retrieving Data via Goose
Goose provides a versatile and extensible architecture for defining types of source/raw data, and function for retrieving data. the abstract class Data_Type from goose.data.data_types defines the template for data types. Built-in, goose provides the following data types and retrieval sources in goose.data.built_in_data_types:
* results data; data on completed games; provides (default) retrieval function from source UnderStats via soccerdata
* standings data; data on a competition's standings; provides (default) retrieval function from source Sofascore via soccerdata
* schedule data; data on schedule of matches; provides (default) retrieval function from source ESPN via soccerdata, and also retrieval function from source UnderStats (via reconstruction).

Custom data types can be defined as follows:
* a new data type can be created via ```python Data_Type.Create_Type(data_type_name, data_retrieval_contract, data_type_description)```
* a new data retrieval function can be defined and associated with a data type via decorator ```python @data_type.Define_Data_Retrieval_Function(source_name, source_description)```

### Discovery and Goose CLI
Goose offers a CLI to facilitate the model development process. Not only does it supply built-in commands, but Goose has the ability to "discover" structures defined recursively deeper than the cwd where "goose ..." is run, and thereby generate associated commands and functionality. Notably:
* Goose can discover built-in and custom-defined operations. These, along with built-in operations, are accessible as "goose ..." CLI commands.
* Goose can discover .fgm model definitions. They can be loaded and employed via referencing them by name.
* Goose can discover Model subclasses that define model definitions. To make a model definition discoverable, apply decorator ```python @define_model(model_definition_name, model_definition_description)```
* Goose can discover built-in and custom-defined data types and data retrieval functions. (data_type).Set_Source() allows for globally setting what data retrieval function to be active. 
* "goose discover" will display every custom and built-in structure that Goose succeeds at discovering

For a complete run-down of built-in functionalities, run "goose --help"
