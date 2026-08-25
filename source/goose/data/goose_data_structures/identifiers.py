# for data manipulation
import pandas as pd
from typing import Self

# for standardizing team names
from goose.data.name_standardization import Team_Name_Mappings, League_Name_Mappings

# struct for storing a specific team
class Team:
    # upon initialized, adjusts team name to standardized Goose equivalent
    def __init__(self, team_name : str):
        self.team = self.standardize_team_name(team_name)

    # Return the standardized name according to provided alias
    @staticmethod
    def standardize_team_name(alias : str):
        return Team_Name_Mappings[alias]

    # Standardizes team names from various aliases used by sources to chosen set of names
    @staticmethod
    def standardize_team_names(team_names : pd.Series):
        return team_names.map(Team_Name_Mappings).fillna(team_names)
    
    # equivalence of teams
    def __eq__(self, other):
        if not isinstance(other, Team):
            return False
        return self.team == other.team
    
    # string alphabetical ordering of teams
    def __lt__(self, other):
        if not isinstance(other, Team):
            return NotImplemented
        return self.team < other.team
    
    # hashing
    def __hash__(self):
        return hash(self.team)
    
    # for df printing
    def __repr__(self):
        return self.team

    # For print() and CSV exports
    def __str__(self):
        return self.team
    
# struct for storing a specific league
class League:
    # upon initialization, adjusts league name to standardized Goose equivalent
    def __init__(self, league_name : str):
        self.league = self.standardize_league_name(league_name)

    # Return the standardized league name according to provided alias
    @staticmethod
    def standardize_league_name(alias : str):
        return League_Name_Mappings[alias]

    # standardize league names from various aliases used by sources to chosen set of names
    @staticmethod
    def standardize_league_names(league_names : pd.Series):
        return league_names.map(League_Name_Mappings).fillna(league_names)

    # equivalence of league
    def __eq__(self, other):
        if not isinstance(other, League):
            return False
        return self.league == other.league
    
    # hashing
    def __hash__(self):
        return hash(self.league)
    
    # for df printing
    def __repr__(self):
        return self.league

    # For print() and CSV exports
    def __str__(self):
        return self.league
    
    # naming scheme conversion for Goose League --> soccerdata api
    @property
    def soccerdata_league_translations(self):
        return {
            League("EPL") : "ENG-Premier League",
            League("LaLiga") : "ESP-La Liga",
            League("Bun") : "GER-Bundesliga",
            League("SerieA") : "ITA-Serie A",
            League("Ligue1") : "FRA-Ligue 1"
        }

    # Goose League --> soccerdata api translation converter
    def to_soccerdata_name(self):
        return self.soccerdata_league_translations[self]

    # naming scheme conversion for Goose League --> ScraperFC
    @property
    def scraperfc_league_translations(self):
        return {
            League("EPL") : "England Premier League",
            League("LaLiga") : "Spain La Liga",
            League("Bun") : "Germany Bundesliga",
            League("SerieA") : "Italy Serie A",
            League("Ligue1") : "France Ligue 1",
            League("UCL") : "UEFA Champions League",
            League("WC") : "FIFA World Cup"
        }

    # Goose League --> scraperfc api translation converter
    def to_scraperfc_name(self):
        return self.scraperfc_league_translations[self]
    
# struct for storing a specific season
class Season:
    # season is stored as the starting (or only) year integer and
    # end_year defaults to start_year if not specified
    # ex. 2025
    def __init__(self, start_year : int, end_year : int = None):
        self.start_year = start_year
        self.end_year = self.start_year if end_year is None else end_year
    
    # equivalence of Season
    def __eq__(self, other):
        if not isinstance(other, Season):
            return False
        return self.start_year == other.start_year
    
    # hashing
    def __hash__(self):
        return hash(self.start_year)

    # for df printing
    def __repr__(self):
        return self.start_year

    # For print() and CSV exports
    def __str__(self):
        return self.start_year
    
    # Goose Season --> soccerdata api year label/tag
    def to_soccerdata_tag(self) -> int:
        return self.start_year
    
    # Goose Season --> ScraperFC Sofascore api year lable/tag
    def to_scraperfc_sofascore_tag(self) -> str:
        # if single-year competition
        if self.start_year == self.end_year:
            return str(self.start_year)
        # if multi-year competition
        else:
            start_short = self.start_year % 100
            end_short = (self.start_year + 1) % 100
            return f"{start_short:02d}/{end_short:02d}"