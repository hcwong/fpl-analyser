import fplrequests

import argparse
import re
import os
from dotenv import load_dotenv
load_dotenv()

# FPL_URL = "https://fantasy.premierleague.com/drf/"
# USER_SUMMARY_SUBURL = "element-summary/"
# LEAGUE_CLASSIC_STANDING_SUBURL = "leagues-classic-standings/"
# LEAGUE_H2H_STANDING_SUBURL = "leagues-h2h-standings/"
# TEAM_ENTRY_SUBURL = "entry/"
# PLAYERS_INFO_SUBURL = "bootstrap-static"
# PLAYERS_INFO_FILENAME = './results/allPlayerInfo.json'

# USER_SUMMARY_URL = FPL_URL + USER_SUMMARY_SUBURL
# PLAYERS_INFO_URL = FPL_URL + PLAYERS_INFO_SUBURL

def main():
    parser = argparse.ArgumentParser(description='Visualize Players picked in a certain gameweek')
    parser.add_argument('-g','--gameweek', help='gameweek number', required=True)
    parser.add_argument('-t', '--type', help='league type')
    args = vars(parser.parse_args())

    pageCount = 1
    GWNumber = args['gameweek']
    leagueIdSelected = os.environ['LEAGUE_ID']   

    #if the file does not exist, then throw error and prompt download
    #should probably abstract out the get playerand captain number function into two 
    for (f in os.listdir('./../results')):
        if (re.match('/{leagueIdSelected}-GW/gi')):
            #TODO: Implement Visualization here
            print('Visualization yet to be implemented')
            break
        else:
            raise FileNotFoundError('Could not find file. Please call fplrequests.py with the relevant arguments')


if __name__ == "__main__":
    main()

