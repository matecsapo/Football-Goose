# Football-G.O.O.S.E.

**Football/soccer (G)eneralized f(O)recast m(O)dels and (S)imulation (E)ngine.**

Football-Goose consists of two parts:
* a set of models for forecasting soccer games/competitions
* a generalized and customizable engine for producing simulations/expectations/predictions of football games and competitions, subject to built-in / user-defined custom model specified to use.

---

### Installation:
Football-Goose is packaged as a pyproject. it can be installed via pip by running the following in your terminal:

```bash
pip install football-goose
```
in terminal. Check pyproject.toml for dependencies and other details.

### goose.engine
The goose.engine subpackage contains the goose simuilation engine. It provides a means of defining a custom / built-in model as a subclass of the abstract goose.engine.model.Model class. Any subclass of model can then invoke the engines various expectation/simulation/prediction functionalities

#### goose.engine.model
defines goose.engine.model.Model, the absract class defining required operations/behaviours of models for interactability with goose.engine. Namely, all concrete models M must implement:
* M.Predict_Game
* M.Simulate_Game
* M.Save_Model
* M.Load_Model

#### goose.engine.forecast
in goose, a forecast defines a means/logic of predicting/expecting/simulation a game, set of games, or a competitions season until completion, subject to the model to use. goose.engine.forecast can be subclassed to implement custom prediction logics or support for custom competitions/formats.

#### goose.engine.league_forecast
defines goose.engine.league_forecast.League_Forecast, which provides functionality, via subclasses League_Expect_Forecast and League_Simulate_Forecast, to, expect-out and simulate-out, respectively, a league-style competition

#### goose.engine.monte_carlo
Implements the running of a monte carlo simulation according to the forecast to use as simulator. Since all competitions differ, a concrete monte-carlo simulator for a given competition is implemented by creating a concrete subclass of goose.engine.monte_carlo.Monte_Carlo_Simulation, thereby defining the competition-specific "interpretation" of the simulations result. 

---

### goose.models
Provides a set of goose.engine compatible models:

* **goose.models.static_poi_reg_model.Static_Poi_Reg_Model**: is a Poisson Regression Model that works by estimating a static [att, def] strength evaluation of all teams in the league
