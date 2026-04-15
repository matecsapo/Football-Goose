# for data manipulation
import pandas as pd

# standardized version of each team's name, accounting for all variety of names used by different sources
    # [chosen name] --> [alias names, ...]
Raw_Team_Name_Mappings = {
    # --- EPL ---
    "AFC Bournemouth": ["Bournemouth", "Bournemouth AFC"],
    "Arsenal": ["Arsenal FC"],
    "Aston Villa": ["Aston Villa FC", "Villa"],
    "Brighton & Hove Albion": ["Brighton", "Brighton and Hove Albion", "Brighton & Hove", "Brighton & HA"],
    "Brentford": ["Brentford FC"],
    "Burnley": ["Burnley FC"],
    "Chelsea": ["Chelsea FC"],
    "Crystal Palace": ["Crystal Palace FC", "CPFC"],
    "Everton": ["Everton FC"],
    "Fulham": ["Fulham FC"],
    "Leeds United": ["Leeds", "Leeds Utd", "Leeds U"],
    "Leicester City": ["Leicester"],
    "Liverpool": ["Liverpool FC"],
    "Manchester City": ["Man City", "Manchester City FC", "MCFC"],
    "Manchester United": ["Man Utd", "Man United", "Manchester United FC", "MUFC"],
    "Newcastle United": ["Newcastle", "Newcastle Utd", "NUFC"],
    "Nottingham Forest": ["Nottm Forest", "Nottingham", "Forest", "Nott'm Forest"],
    "Sheffield United": ["Sheffield Utd", "Sheff Utd", "Sheffield U"],
    "Sunderland": ["Sunderland AFC", "Sunderland WFC"],
    "Tottenham Hotspur": ["Tottenham", "Spurs", "Tottenham Hotspur FC"],
    "West Ham United": ["West Ham", "West Ham Utd", "WHUFC"],
    "Wolverhampton Wanderers": ["Wolverhampton", "Wolves", "Wolves FC"],

    # --- LA LIGA ---
    "Alavés": ["Alaves", "Deportivo Alavés"],
    "Athletic Club": ["Athletic Bilbao", "Athletic", "Bilbao"],
    "Atlético Madrid": ["Atletico Madrid", "Atlético", "Atleti", "Atlético de Madrid"],
    "Barcelona": ["Barca", "FC Barcelona", "FCB"],
    "Celta Vigo": ["Celta", "Celta de Vigo", "RC Celta"],
    "Espanyol": ["RCD Espanyol"],
    "Getafe": ["Getafe CF"],
    "Girona": ["Girona FC"],
    "Las Palmas": ["UD Las Palmas"],
    "Leganés": ["Leganes", "CD Leganés"],
    "Mallorca": ["RCD Mallorca"],
    "Osasuna": ["CA Osasuna"],
    "Rayo Vallecano": ["Rayo", "Vallecano"],
    "Real Betis": ["Betis", "Real Betis Balompié"],
    "Real Madrid": ["Real", "Madrid", "Los Blancos"],
    "Real Sociedad": ["Sociedad", "La Real", "R Sociedad"],
    "Sevilla": ["Sevilla FC"],
    "Valencia": ["Valencia CF"],
    "Valladolid": ["Real Valladolid"],
    "Villarreal": ["Villarreal CF"],

    # --- BUNDESLIGA ---
    "Augsburg": ["FC Augsburg", "FCA"],
    "Bayer Leverkusen": ["Leverkusen", "Bayer 04 Leverkusen", "B04"],
    "Bayern Munich": ["Bayern München", "Bayern", "FC Bayern", "FCB"],
    "Bochum": ["VfL Bochum"],
    "Borussia Dortmund": ["Dortmund", "BVB", "BVB 09"],
    "Borussia Mönchengladbach": ["Mönchengladbach", "Gladbach", "M'gladbach", "BMG"],
    "Eintracht Frankfurt": ["Frankfurt", "Eintracht", "SGE"],
    "Freiburg": ["SC Freiburg"],
    "Heidenheim": ["1. FC Heidenheim"],
    "Hoffenheim": ["TSG Hoffenheim", "TSG 1899 Hoffenheim"],
    "Holstein Kiel": ["Kiel"],
    "Mainz 05": ["Mainz", "1. FSV Mainz 05"],
    "RB Leipzig": ["Leipzig", "RasenBallsport Leipzig"],
    "St. Pauli": ["FC St. Pauli"],
    "Stuttgart": ["VfB Stuttgart"],
    "Union Berlin": ["1. FC Union Berlin"],
    "Werder Bremen": ["Bremen", "Werder"],
    "Wolfsburg": ["VfL Wolfsburg"],

    # --- SERIE A ---
    "AC Milan": ["Milan", "ACM"],
    "Atalanta": ["Atalanta BC"],
    "Bologna": ["Bologna FC"],
    "Cagliari": ["Cagliari Calcio"],
    "Como": ["Como 1907"],
    "Empoli": ["Empoli FC"],
    "Fiorentina": ["ACF Fiorentina"],
    "Genoa": ["Genoa CFC"],
    "Inter Milan": ["Inter", "Internazionale", "Inter Nazionale Milano"],
    "Juventus": ["Juve", "Vecchia Signora"],
    "Lazio": ["SS Lazio"],
    "Monza": ["AC Monza"],
    "Napoli": ["SSC Napoli"],
    "Parma": ["Parma Calcio"],
    "Roma": ["AS Roma"],
    "Torino": ["Torino FC"],
    "Udinese": ["Udinese Calcio"],
    "Venezia": ["Venezia FC"],
    "Verona": ["Hellas Verona"],

    # --- LIGUE 1 ---
    "Angers": ["Angers SCO"],
    "Auxerre": ["AJ Auxerre"],
    "Brest": ["Stade Brestois 29"],
    "Havre": ["Le Havre", "Le Havre AC", "HAC"],
    "Lens": ["RC Lens"],
    "Lille": ["Lille OSC", "LOSC"],
    "Lyon": ["Olympique Lyonnais", "OL"],
    "Marseille": ["Olympique de Marseille", "OM"],
    "Monaco": ["AS Monaco"],
    "Montpellier": ["Montpellier HSC"],
    "Nantes": ["FC Nantes"],
    "Nice": ["OGC Nice"],
    "Paris Saint-Germain": ["PSG", "Paris SG", "Paris S-G"],
    "Reims": ["Stade de Reims"],
    "Rennes": ["Stade Rennais"],
    "Saint-Étienne": ["Saint-Etienne", "ASSE"],
    "Strasbourg": ["RC Strasbourg"],
    "Toulouse": ["Toulouse FC"]
}

# Easily applicable flattened version of the mappings
    # gets created the first time in execution that team_names module is imported
Team_Name_Mappings = {}
for chosen, aliases in Raw_Team_Name_Mappings.items():
    # map chosen to itself
    Team_Name_Mappings[chosen] = chosen # Map clean to itself
    # map aliases to chosen
    for alias in aliases:
        Team_Name_Mappings[alias] = chosen

# Return the standardized name according to provided alias
def standardize_name(alias : str):
    return Team_Name_Mappings[alias]

# Standardizes team names from various aliases used by sources to chosen set of names
def standardize_names(team_names : pd.Series):
    return team_names.map(Team_Name_Mappings).fillna(team_names)
