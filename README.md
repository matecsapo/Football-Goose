# Football-G.O.O.S.E.

**Football/soccer (G)eneralized f(O)recast m(O)dels and (S)imulation (E)ngine.**

Football-Goose is a modular python framework designed to faciliate building of models to predict/simulate football/soccer matches and competitions. Football-Goose consists of two core subpackages:
* goose.models --> a set of models for forecasting football games/competitions
* goose.engine --> a generalized, model-agnostic football simulation environment. The engine is built for extensibility and customizability, allowing users to generate match expectations and tournament outcomes using either built-in "Goose Native" goose.models or custom, user-defined implementations.

---

### Installation and Getting Started:
Football-Goose is packaged as a pyproject. it can be installed via pip by running

```bash
pip install git+https://github.com/matecsapo/football-goose.git
```
in terminal. Check pyproject.toml for dependencies and other details. I strongly recommend reading the rest of README.md, below, to familiarze oneself with the engine, as well the available native goose.models!

### goose.engine
subpackage goose.engine houses the football simulation logic and functionalities. goose.engine.model defines the "contract" for model integeration
into the engine. By employing (via instantiating) and/or extending (via subclassing) the provided interfaces, goose.engine's built-in functionalities to run complex expectations, simulations, and predictive workflows.

#### goose.engine.model
defines goose.engine.model.Model, the absract base class defining required operations/behaviours of models for interactability with goose.engine. Namely, all concrete models M must be suclasses of class Model that implement:
* M.Predict_Game --> Generate a set of predictive info for specified game
* M.Simulate_Game --> Simulate an occurence of specified game

#### goose.engine.forecast
in goose, a forecast class encapsulates the logic of predicting/expecting/simulation a match, set of matches, or a competition's entire season, according to a given model. This module is designed for extensibility, allowing users to subclass base forecast objects to implement custom prediction heuristics or support unique tournament formats.

#### goose.engine.league_forecast
Provides a forecast for league-style (i.e. round-robin like PL, not KO like CL) competitions. It provides two main forecasting approaches:
* League_Expect_Forecast: Uses expected values to project standings.
* League_Simulate_Forecast: Uses game-by-game simulation to "play" out remaining fixtures.

#### goose.engine.monte_carlo
Provides the infrastructure for high-iteration Monte Carlo experiments. Because every competition has a unique "success" definition (e.g., Top 4 vs. Relegation), a competition-specific concrete Monte_Carlo_Simulation subclass is used to define the competition-specific interpretation and aggregation of simulation results.

---

### goose.models
A collection of Football-Goose "native" models built on, and that fully integrate with, the goose.engine interface:

* **goose.models.static_poi_reg_model.Static_Poi_Reg_Model**: is a Poisson Regression Model that works by estimating a static [att, def] strength evaluation of all teams in the league

#### goose.models.goose_trained_models
A set of fully trained models available to use for prediction. These models are for "live" forecasting from now through season end, and are therefore refreshed frequently to re-train on the latest match data.
