import requests
from fplanalyzer.definitions import FPL_ROOT, FPL_BOOTSTRAP, MAX_GAMEWEEK, MIN_GAMEWEEK, FPL_USER_HISTORY, FPL_CLASSIC_LEAGUE
from fplanalyzer.fpl_api_structs import User

"""
Returns the current active gameweek in the form of an int
"""
def get_current_gameweek():
    try:
        response = requests.get(f"{FPL_ROOT}{FPL_BOOTSTRAP}")
        response = response.json()
        return [r["id"] for r in response["events"] if r["is_current"]][0]

    except Exception as e:
        print(f"Error occured while getting current gameweek: {e}")
        return -1

def is_gameweek_valid(gameweek_int):
    return gameweek_int >= MIN_GAMEWEEK and gameweek_int <= MAX_GAMEWEEK and gameweek_int <= get_current_gameweek()

"""
Gets all the players in the league:
However, no pagination supported, so max of 50 players allowed
"""
def get_league_users(league_id):
    users = []

    try:
        response = requests.get(FPL_ROOT + FPL_CLASSIC_LEAGUE.format(league_id))
        response = response.json()
        for user in response["standings"]["results"]:
            users.append(User(user["id"], user["total"], user["entry"], user["entry_name"], user["player_name"]))
    except Exception as e:
        raise Exception(f"Could not get league players: {e}")

    return users

def get_player_gameweek_interval(user_entry, start_gameweek_int, end_gameweek_int):
    if not is_gameweek_valid(start_gameweek_int) or not is_gameweek_valid(end_gameweek_int)\
    or start_gameweek_int > end_gameweek_int:
        raise ValueError("Gameweek invalid")

    try:
        response = requests.get(FPL_ROOT + FPL_USER_HISTORY.format(user_entry))
        response = response.json()

        points = 0
        for gw in response["current"]:
            if gw["event"] < start_gameweek_int or gw["event"] > end_gameweek_int:
                continue
            points += (gw["points"] - gw["event_transfers_cost"])

        return points
    except Exception as e:
        raise Exception(f"Failed to get user history: {e}, {user_entry}")

