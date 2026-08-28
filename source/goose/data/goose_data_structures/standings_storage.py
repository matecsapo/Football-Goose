# for creating templates
from abc import ABC

# for data maniuplation and handling
from goose.data.goose_data_structures.identifiers import League, Season
import pandas as pd
import pandera.pandas as pa

# struct for storing a given competition's standings
# Abstracted - implemented for various concrete competition styles (i.e. round-robin, KO, etc.)
# standings are stored in self.standings
class Standings(ABC):
    # Standings must specify [league, season]
    def __init__(self, league : League = None, season : Season = None):
        self.league = league
        self.season = season
        # for storing [league, season]'s standings
        self.standings = None
    
    # save
    def save(self, path):
        pass

    # view
    def view(self):
        pass

# struct for storing table-style standings
# Abstracted - implemented for specific type of tabled standings
# Tables store standings as pd dataframe satisfiying specified schema
class Table(Standings, ABC):
    # pd dataframe schema
    # each concrete Table standings table type implements
    Table_Schema : pa.DataFrameSchema = None

    # Constructed by immediately validating supplied dataframe according to pandera league table schema
    def __init__(self, league_table : pd.DataFrame, league : League = None, season : Season = None):
        super().__init__(league, season)
        # Enforce league_table as being of required League_Table_Schema pd dataframe schema
        self.standings : pd.DataFrame = league_table
        self.standings = self.Table_Schema.validate(self.standings)

    # sipmlifies standings to just rows of Table_Schem
    def simplify(self):
        self.standings = self.standings[list(self.Table_Schema.columns.keys())]

    # save data
    def save(self, path):
        self.standings.to_csv(path)
    
    # view data
    def view(self):
        print(self.standings.head(20))

# struct for storing a given [league, season] league=round-robin - style-competition standings
# A League_Table must have:
    # Team, MP, Pts, GD
    # Can have any additional columns, as desired
class League_Table(Table):
    # Pandera schema defining league tabble daf
    Table_Schema = pa.DataFrameSchema(
        columns = {
            "Team": pa.Column(object),
            "MP":   pa.Column(int, pa.Check.ge(0)), # MP must be >= 0
            "Pts":  pa.Column(int, pa.Check.ge(0)), # Pts must be >= 0
            "GD":   pa.Column(int)
        },
        # Additional columns are allowed
        strict = False, 
        # Types will automatically be recast, if natural
        coerce = True  
    )

# a struct for storing x-pected standings for a given [league, season] league-style competition
# A Expected_Table must have:
    # Team MP, xPts, xGD
    # Can have any additional columns, as desired
class Expected_Table(Table):
    # Pandera schema defining league tabble daf
    Table_Schema = pa.DataFrameSchema(
        columns = {
            "Team": pa.Column(object),
            "MP":   pa.Column(int, pa.Check.ge(0)), # MP must be >= 0
            "xPts":  pa.Column(float, pa.Check.ge(0)), # Pts must be >= 0
        },
        # Additional columns are allowed
        strict = False, 
        # Types will automatically be recast, if natural
        coerce = True  
    )

# a struct for storing simulated standings for a given [league, season] league-style competition
# A Simulated_Tabled must have:
    # Team, MP, Simulated Pts, Simulated GD
    # Can have any additoinal columns, as desired
class Simulated_Table(Table):
    # Pandera schema defining league tabble daf
    Table_Schema = pa.DataFrameSchema(
        columns = {
            "Team": pa.Column(object),
            "MP":   pa.Column(int, pa.Check.ge(0)), # MP must be >= 0
            "Simulated Pts":  pa.Column(int, pa.Check.ge(0)), # Pts must be >= 0
            "Simulated GD":   pa.Column(int),
        },
        # Additional columns are allowed
        strict = False, 
        # Types will automatically be recast, if natural
        coerce = True  
    )