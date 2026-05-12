# standardized version of each team's name, accounting for all variety of names used by different sources
    # [chosen name] --> [alias names, ...]
Raw_Team_Name_Mappings = {
    # --- EPL ---
    "AFC Bournemouth": ["Bournemouth", "Bournemouth AFC", "A.F.C. Bournemouth"],
    "Arsenal": ["Arsenal FC", "AFC"],
    "Aston Villa": ["Aston Villa FC", "Villa", "AVFC"],
    "Brighton & Hove Albion": ["Brighton", "Brighton and Hove Albion", "Brighton & Hove", "Brighton & HA", "BHAFC"],
    "Brentford": ["Brentford FC"],
    "Burnley": ["Burnley FC"],
    "Chelsea": ["Chelsea FC"],
    "Crystal Palace": ["Crystal Palace FC", "CPFC", "Palace"],
    "Everton": ["Everton FC"],
    "Fulham": ["Fulham FC"],
    "Ipswich Town": ["Ipswich", "Ipswich Town FC"], # Added for 2024+
    "Leeds United": ["Leeds", "Leeds Utd", "Leeds U", "LUFC"],
    "Leicester City": ["Leicester", "LCFC"],
    "Liverpool": ["Liverpool FC", "LFC"],
    "Manchester City": ["Man City", "Manchester City FC", "MCFC", "City"],
    "Manchester United": ["Man Utd", "Man United", "Manchester United FC", "MUFC", "United"],
    "Newcastle United": ["Newcastle", "Newcastle Utd", "NUFC"],
    "Nottingham Forest": ["Nottm Forest", "Nottingham", "Forest", "Nott'm Forest", "N Forest"],
    "Sheffield United": ["Sheffield Utd", "Sheff Utd", "Sheffield U", "SUFC"],
    "Sunderland": ["Sunderland AFC", "Sunderland WFC"],
    "Tottenham Hotspur": ["Tottenham", "Spurs", "Tottenham Hotspur FC", "THFC"],
    "West Ham United": ["West Ham", "West Ham Utd", "WHUFC", "The Hammers"],
    "Wolverhampton Wanderers": ["Wolverhampton", "Wolves", "Wolves FC", "WWFC"],

    # --- LA LIGA ---
    "Alavés": ["Alaves", "Deportivo Alavés", "Dep. Alaves"],
    "Athletic Club": ["Athletic Bilbao", "Athletic", "Bilbao", "Athletic Club Bilbao"],
    "Atlético Madrid": ["Atletico Madrid", "Atlético", "Atleti", "Atlético de Madrid", "At Madrid"],
    "Barcelona": ["Barca", "FC Barcelona", "FCB", "Barça"],
    "Celta Vigo": ["Celta", "Celta de Vigo", "RC Celta", "RC Celta de Vigo"],
    "Espanyol": ["RCD Espanyol", "Espanyol Barcelona"],
    "Getafe": ["Getafe CF", "Getafe"],
    "Girona": ["Girona FC"],
    "Las Palmas": ["UD Las Palmas", "L Palmas"],
    "Leganés": ["Leganes", "CD Leganés", "C.D. Leganés"],
    "Mallorca": ["RCD Mallorca", "Mallorca"],
    "Osasuna": ["CA Osasuna", "Osasuna"],
    "Rayo Vallecano": ["Rayo", "Vallecano", "Rayo Vallecano de Madrid"],
    "Real Betis": ["Betis", "Real Betis Balompié", "R. Betis"],
    "Real Madrid": ["Real", "Madrid", "Los Blancos", "R Madrid"],
    "Real Sociedad": ["Sociedad", "La Real", "R Sociedad", "R. Sociedad"],
    "Sevilla": ["Sevilla FC", "Sevilla"],
    "Valencia": ["Valencia CF", "Valencia"],
    "Valladolid": ["Real Valladolid", "Valladolid"],
    "Villarreal": ["Villarreal CF", "Villarreal"],
    "Elche": ["Elche CF", "Elche", "Elche Club de Fútbol"],
    "Levante": ["Levante UD", "Levante", "Levante Unión Deportiva", "LUD"],
    "Real Oviedo": ["Oviedo", "Real Oviedo", "Real Oviedo SAD", "Real Uviéu"],

    # --- BUNDESLIGA ---
    "Augsburg": ["FC Augsburg", "FCA", "Augsburg FC", "Augsbourg"],
    "Bayer Leverkusen": ["Leverkusen", "Bayer 04 Leverkusen", "B04", "Bayer", "B. Leverkusen"],
    "Bayern Munich": ["Bayern München", "Bayern Munchen", "Bayern Muenchen", "Bayern", "FC Bayern", "FCB", "FC Bayern München", "FC Bayern Munich"],
    "Bochum": ["VfL Bochum", "VfL {Bochum 1848", "Bochum 1848"],
    "Borussia Dortmund": ["Dortmund", "BVB", "BVB 09", "Bor. Dortmund", "Borussia Dortmd"],
    "Borussia Mönchengladbach": ["Mönchengladbach", "Moenchengladbach", "Monchengladbach", "Gladbach", "M'gladbach", "BMG", "Borussia M.Gladbach", "Borussia M'gladbach"],
    "Eintracht Frankfurt": ["Frankfurt", "Eintracht", "SGE", "E. Frankfurt"],
    "FC Cologne": ["Köln", "Koln", "Koeln", "FC Köln", "Cologne", "1. FC Köln", "1. FC Koeln"],
    "Freiburg": ["SC Freiburg", "Freiburg SC", "SCF"],
    "Hamburger SV": ["HSV", "Hamburg", "Hamburger", "Hamburg SV"],
    "Heidenheim": ["1. FC Heidenheim", "1. FC Heidenheim 1846", "FCH", "FC Heidenheim", "Heidenh'm"],
    "Hoffenheim": ["TSG Hoffenheim", "TSG 1899 Hoffenheim", "Hoffenheim TSG", "1899 Hoffenheim"],
    "Holstein Kiel": ["Kiel", "Holstein", "KSV Holstein", "Holstein Kiel KSV"],
    "Mainz 05": ["Mainz", "1. FSV Mainz 05", "Mainz 05 FSV", "FSV Mainz"],
    "RB Leipzig": ["Leipzig", "RasenBallsport Leipzig", "Red Bull Leipzig", "RBL"],
    "St. Pauli": ["FC St. Pauli", "St Pauli", "St.Pauli"],
    "Stuttgart": ["VfB Stuttgart", "Stuttgart VfB", "VfB"],
    "Union Berlin": ["1. FC Union Berlin", "Union Berlin", "FC Union"],
    "Werder Bremen": ["Bremen", "Werder", "SV Werder Bremen", "Werder Brem"],
    "Wolfsburg": ["VfL Wolfsburg", "Wolfsburg VfL", "VfL"],

    # --- SERIE A ---
    "AC Milan": ["Milan", "ACM", "A.C. Milan"],
    "Atalanta": ["Atalanta BC", "Atalanta"],
    "Bologna": ["Bologna FC", "Bologna 1909"],
    "Cagliari": ["Cagliari Calcio", "Cagliari"],
    "Como": ["Como 1907", "Como"],
    "Empoli": ["Empoli FC", "Empoli"],
    "Fiorentina": ["ACF Fiorentina", "Fiorentina"],
    "Genoa": ["Genoa CFC", "Genoa"],
    "Inter Milan": ["Inter", "Internazionale", "Inter Nazionale Milano", "Inter Milan"],
    "Juventus": ["Juve", "Vecchia Signora", "Juventus FC"],
    "Lazio": ["SS Lazio", "Lazio"],
    "Monza": ["AC Monza", "Monza"],
    "Napoli": ["SSC Napoli", "Napoli"],
    "Parma": ["Parma Calcio", "Parma Calcio 1913", "Parma"],
    "Roma": ["AS Roma", "Roma"],
    "Torino": ["Torino FC", "Torino"],
    "Udinese": ["Udinese Calcio", "Udinese"],
    "Venezia": ["Venezia FC", "Venezia"],
    "Verona": ["Hellas Verona", "Verona"],
    "Sassuolo": ["US Sassuolo", "Sassuolo Calcio", "U.S. Sassuolo"],
    "Cremonese": ["US Cremonese", "Cremonese Calcio", "U.S. Cremonese 1903"],
    "Lecce": ["US Lecce", "U.S. Lecce", "Lecce Calcio"],
    "Pisa": ["Pisa SC", "Pisa 1909", "A.C. Pisa", "Pisa Sporting Club"],

    # --- LIGUE 1 ---
    "Angers": ["Angers SCO", "Angers-SCO", "SCO Angers", "Angers"],
    "Auxerre": ["AJ Auxerre", "Auxerre AJ", "AJA", "A.J. Auxerre"],
    "Brest": ["Stade Brestois 29", "Stade Brestois", "Brestois", "Brest 29", "SB29"],
    "Havre": ["Le Havre", "Le Havre AC", "HAC", "Le Havre A.C.", "Le Havre", "Havre AC"],
    "Lens": ["RC Lens", "Lens RC", "RCL", "Racing Club de Lens"],
    "Lille": ["Lille OSC", "LOSC", "Lille", "Lille Metropole", "LOSC Lille"],
    "Lyon": ["Olympique Lyonnais", "OL", "Lyon", "Olympique Lyon"],
    "Marseille": ["Olympique de Marseille", "OM", "Marseille", "Olympique Marseille"],
    "Monaco": ["AS Monaco", "Monaco", "ASM", "AS Monaco FC"],
    "Montpellier": ["Montpellier HSC", "Montpellier", "MHSC", "Montpellier Herault"],
    "Nantes": ["FC Nantes", "Nantes", "FCN", "FC Nantes Atlantique"],
    "Nice": ["OGC Nice", "Nice", "OGCN", "OGC Nice Cote d'Azur"],
    "Paris Saint-Germain": ["PSG", "Paris SG", "Paris S-G", "Paris Saint Germain", "Paris SG FC", "Paris Saint-Germain FC"],
    "Reims": ["Stade de Reims", "Reims", "SDR", "Stade Reims"],
    "Rennes": ["Stade Rennais", "Rennes", "Stade Rennais FC", "SRFC"],
    "Saint-Étienne": ["Saint-Etienne", "ASSE", "St Etienne", "St-Etienne", "Saint Etienne", "AS Saint-Etienne"],
    "Strasbourg": ["RC Strasbourg", "Strasbourg", "RC Strasbourg Alsace", "RCSA", "Strasbourg RC"],
    "Toulouse": ["Toulouse FC", "Toulouse", "TFC", "Toulouse Football Club"],
    "Lorient": ["FC Lorient", "Lorient FC", "Lorient-Bretagne Sud", "FCL"],
    "Metz": ["FC Metz", "Metz FC", "Football Club de Metz"],
    "Paris FC": ["PFC", "Paris FC", "Paris Football Club"]
}

# standardized version of each league's name, accounting for all variety of names used by different sources
    # [chosen name] --> [alias names, ...]
Raw_League_Name_Mappings = {
    "ENG-Premier League": [
        "Premier League", "EPL", "English Premier League", "Premier League (ENG)", 
        "PL", "England - Premier League", "Premiership", "Prem", "The Prem", 
        "BPL", "Barclays Premier League"
    ],
    "ESP-La Liga": [
        "La Liga", "LaLiga", "Spain - La Liga", "Spanish La Liga", "Primera Division", 
        "Primera División", "LFP", "La Liga Santander", "La Liga EA Sports", 
        "LL", "LaLiga 1"
    ],
    "GER-Bundesliga": [
        "Bundesliga", "German Bundesliga", "Germany - Bundesliga", "Bundesliga 1", 
        "1. Bundesliga", "Buli", "Bun", "German First Division"
    ],
    "ITA-Serie A": [
        "Serie A", "Italy - Serie A", "Italian Serie A", "Serie A TIM", 
        "Calcio", "SerieA", "ITA1"
    ],
    "FRA-Ligue 1": [
        "Ligue 1", "French Ligue 1", "France - Ligue 1", "Ligue 1 Uber Eats", 
        "Ligue 1 McDonald’s", "L1", "Ligue1"
    ],
    "UEFA-Champions League": [
        "Champions League", "UCL", "UEFA Champions League", "Champ League", 
        "Champions", "The Champions League"
    ],
    "UEFA-Europa League": [
        "Europa League", "UEL", "UEFA Europa League", "Europa", "Euro League"
    ],
    "USA-MLS": [
        "MLS", "Major League Soccer", "USA - MLS", "MLS Cup", "US MLS"
    ]
}

# Easily applicable flattened versions of the mappings
    # gets created the first time in execution that team_names module is imported
Team_Name_Mappings = {}
League_Name_Mappings = {}
for raw_source, target in [(Raw_Team_Name_Mappings, Team_Name_Mappings), (Raw_League_Name_Mappings, League_Name_Mappings)]:
    for chosen, aliases in raw_source.items():
        # map chosen to itself
        target[chosen] = chosen # Map clean to itself
        # map aliases to chosen
        for alias in aliases:
            target[alias] = chosen
