import pandas as pd
import matplotlib.pyplot as plt
import argparse
import re
import os

from dotenv import load_dotenv 
load_dotenv()

from .. import definitions
from .fplrequests import getPlayerAndCaptainNumbers

ROOT_DIR = definitions.ROOT_DIR

class Visualizer(object):
    def __init__(self):
        self.data = []

    def readCSV(self, path):
        gwData = pd.read_csv(path, names=None)
        self.data.append(gwData)

    # TODO: Maybe parse the CSV just one time before we download it? So don't have to repeatedly perform this
    def cleanData(self):
        gwDF = self.data[0]
        for index, row in gwDF.iterrows():
           gwDF.at[index,'name'] = re.sub(r'\'|b\'' , "", row['name'])

    def visualize(self):
        self.cleanData()
        self.data[0].plot(kind='bar')
        plt.show() # TODO: Too many bar charts, should select the top 10. Also the x axis is the DF index instead of the player names

def main():
    parser = argparse.ArgumentParser(description='Visualize Players picked in a certain gameweek')
    parser.add_argument('-g','--gameweek', help='gameweek number', required=True)
    args = vars(parser.parse_args())

    leagueStandingUrl = definitions.FPL_URL + definitions.LEAGUE_CLASSIC_STANDING_SUBURL
    pageCount = 1
    GWNumber = args['gameweek']
    leagueIdSelected = os.environ['LEAGUE_ID']  

    visualizer = Visualizer() 

    # if the file does not exist, then throw error and prompt download
    resultsPath = f"{ROOT_DIR}/fplanalyzer/results"
    found = False
    for f in os.listdir(resultsPath):
        if (re.search(f"captain-{leagueIdSelected}-GW{GWNumber}", f)):
            # readCSV(os.path.abspath(f"{resultsPath}/{f}"))
            # For now we are only using the playersPicked data and not captain
            pass
        elif (re.search(f"Picked-{leagueIdSelected}-GW{GWNumber}", f)):
            visualizer.readCSV(os.path.abspath(f"{resultsPath}/{f}"))
            found = True
            break
    if not found: 
        getPlayerAndCaptainNumbers(leagueIdSelected, pageCount, leagueStandingUrl, GWNumber)
        visualizer.readCSV(os.path.abspath(f"{resultsPath}/playersPicked-{leagueIdSelected}-GW{GWNumber}"))
    visualizer.visualize()


if __name__ == "__main__":
    main()