import os

# define project root
PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))

# FPL Urls to call API
FPL_URL = "https://fantasy.premierleague.com/drf/"
FPL_ROOT = "https://fantasy.premierleague.com/api/"
USER_SUMMARY_SUBURL = "element-summary/"
LEAGUE_CLASSIC_STANDING_SUBURL = "leagues-classic-standings/"
LEAGUE_H2H_STANDING_SUBURL = "leagues-h2h-standings/"
TEAM_ENTRY_SUBURL = "entry/"
PLAYERS_INFO_SUBURL = "bootstrap-static"
PLAYERS_INFO_FILENAME = './results/allPlayerInfo.json'
FPL_BOOTSTRAP = "bootstrap-static/"
FPL_USER_HISTORY = "entry/{}/history/"
FPL_CLASSIC_LEAGUE = "leagues-classic/{}/standings/"

USER_SUMMARY_URL = FPL_URL + USER_SUMMARY_SUBURL
PLAYERS_INFO_URL = FPL_URL + PLAYERS_INFO_SUBURL
START_PAGE = 1
MIN_GAMEWEEK, MAX_GAMEWEEK = 1, 38

# Error Messages
ERROR_MSG_GW = "Gameweek start should be >= 1 and gameweek end should be <= current gameweek"
SCORING_COMMAND_PROMPT = "/scoring start_gw end_gw"
ERROR_PLAYERS_LEAGUE = "Error getting players in league"
ERROR_FPL_API_GENERIC = "Error pinging FPL API"
