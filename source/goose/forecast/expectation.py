# for implementing a forecast
from goose.forecast.forecast import Forecast
from goose.data.goose_data_structures.game_storage import Game, Game_Points_Expectation
from abc import ABC, abstractmethod

# for employing a model
from goose.model import Model

# class for performing an expectation forecast
class Expectation(Forecast, ABC):
    # PL_Expext_Forecast requires no special parameters
    def __init__(self, forecast_name : str, model : Model):
        super().__init__(forecast_name, model)
    
    # Returns expected value of goals scored + points achieved by each team in specified game
    @staticmethod
    def Expect_Game(game : Game, model : Model):
        prediction = model.Predict_Game(game)
        # determine xp of both teams
        home_xp = 0 * prediction.prob_away_win + 1 * prediction.prob_draw + 3 * prediction.prob_home_win
        away_xp = 0 * prediction.prob_home_win + 1 * prediction.prob_draw + 3 * prediction.prob_away_win
        # return game points expectation
        return Game_Points_Expectation(game, home_xp, away_xp)
