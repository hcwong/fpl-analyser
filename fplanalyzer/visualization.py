import numpy as np
import matplotlib as plt
import argparse
import re
import os

from dotenv import load_dotenv 
load_dotenv()

from .. import definitions
from .fplrequests import getPlayerAndCaptainNumbers

ROOT_DIR = definitions.ROOT_DIR

# Read the csv and load it into a numpy array
def readCSV(path):
    data = np.genfromtxt(path, delimiter=',')

# TODO: write a function to handle the visualization

# TODO: Maybe store the parsed arrays somewhere? 

def main():
    parser = argparse.ArgumentParser(description='Visualize Players picked in a certain gameweek')
    parser.add_argument('-g','--gameweek', help='gameweek number', required=True)
    args = vars(parser.parse_args())

    leagueStandingUrl = definitions.FPL_URL + definitions.LEAGUE_CLASSIC_STANDING_SUBURL
    pageCount = 1
    GWNumber = args['gameweek']
    leagueIdSelected = os.environ['LEAGUE_ID']   

    # if the file does not exist, then throw error and prompt download
    # TODO: should probably abstract out the get playerand captain number function into two functions
    # TODO: fix the path in listdir, try abspath
    resultsPath = f"{ROOT_DIR}/fplanalyzer/results"
    for f in os.listdir(resultsPath):
        if (re.search(f"captain-{leagueIdSelected}-GW{GWNumber}", f)):
            # readCSV(os.path.abspath(f"{resultsPath}/{f}"))
            # For now we are only using the playersPicked data and not captain
            pass
        else if (re.search(f"Picked-{leagueIdSelected}-GW{GWNumber}", f)):
            readCSV(os.path.abspath(f"{resultsPath}/{f}"))
            break
        else:
            getPlayerAndCaptainNumbers(leagueIdSelected, pageCount, leagueStandingUrl, GWNumber)
           # TODO: call readcsv here as well once above function is done?

# TODO: Make visualization into a class?
# class Visualizer(object):
#     def __init__(self):    


if __name__ == "__main__":
    main()