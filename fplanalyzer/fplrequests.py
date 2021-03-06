'''
Taken from FantasyPremierLeague-Api.py by spinach and modified
https://github.com/spinach/FantasyPremierLeague-Api.py/blob/master/playersPickedInLeague.py
Use this to make calls to the FPL API
'''

import requests
import json
import csv
import argparse
import os
import pathlib
import sys

#load the env variables
# from dotenv import load_dotenv
# load_dotenv()

from .definitions import *

# Download all player data: https://fantasy.premierleague.com/drf/bootstrap-static
def getPlayersInfo():
    try:
        with requests.Session() as s:
            r = s.get(PLAYERS_INFO_URL)        
        jsonResponse = r.json()
        directory = os.path.dirname(PLAYERS_INFO_FILENAME)
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
        with open(PLAYERS_INFO_FILENAME, 'w') as outfile:
            json.dump(jsonResponse, outfile)

    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

# Read player info from the json file that we downlaoded
def getAllPlayersDetailedJson():
    with open(PLAYERS_INFO_FILENAME) as json_data:
        d = json.load(json_data)
        return d

# Maps the player ID to the name
def mapPlayerNametoID():
    getPlayersInfo()
    playerElementIdToNameMap = {}
    allPlayers = getAllPlayersDetailedJson()
    for element in allPlayers["elements"]:
        playerElementIdToNameMap[element["id"]] = element["web_name"].encode('ascii', 'ignore')
    return playerElementIdToNameMap


# Get users in league: https://fantasy.premierleague.com/drf/leagues-classic-standings/336217?phase=1&le-page=1&ls-page=5
def getUserEntryIds(league_id, ls_page, league_Standing_Url):
    league_url = league_Standing_Url + str(league_id) + "?phase=1&le-page=1&ls-page=" + str(ls_page)
    try:
        with requests.Session() as s:
            r = s.get(league_url)
        jsonResponse = r.json()
        standings = jsonResponse["standings"]["results"]
        if not standings:
            print("no more standings found!")
            return None
        entries = []
        for player in standings:
            entries.append(player["entry"])
        return entries 

    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

# Team picked by user. example: https://fantasy.premierleague.com/drf/entry/2677936/event/1/picks with 2677936 being entry_id of the player
def getplayersPickedForEntryId(entry_id, GWNumber):
    eventSubUrl = "event/" + str(GWNumber) + "/picks"
    playerTeamUrlForSpecificGW = FPL_URL + TEAM_ENTRY_SUBURL + str(entry_id) + "/" + eventSubUrl
    try:
        with requests.Session() as s:
            r = s.get(playerTeamUrlForSpecificGW)
        jsonResponse = r.json()
        picks = jsonResponse["picks"]
        elements = []
        captainId = 1
        for pick in picks:
            elements.append(pick["element"])
            if pick["is_captain"]:
                captainId = pick["element"]

        return elements, captainId
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

# Calculate the number of players and captains picked for gameweek
def getPlayerAndCaptainNumbers(leagueIdSelected, pageCount, leagueStandingUrl, GWNumber):
    
    # Get all the player information in a csv file and then map the names to id
    allPlayers = mapPlayerNametoID()
    countOfPlayersPicked = {}
    countOfCaptainsPicked = {}
    totalNumberOfPlayersCount = 0

    while (True):
        try:
            entries = getUserEntryIds(leagueIdSelected, pageCount, leagueStandingUrl)
            if entries is None:
                print("breaking as no more player entries")
                break

            totalNumberOfPlayersCount += len(entries)
            print("parsing pageCount: " + str(pageCount) + " with total number of players so far:" + str(
                totalNumberOfPlayersCount))
            for entry in entries:
                elements, captainId = getplayersPickedForEntryId(entry, GWNumber)
                for element in elements:
                    name = allPlayers[element]
                    if name in countOfPlayersPicked:
                        countOfPlayersPicked[name] += 1
                    else:
                        countOfPlayersPicked[name] = 1

                captainName = allPlayers[captainId]
                if captainName in countOfCaptainsPicked:
                    countOfCaptainsPicked[captainName] += 1
                else:
                    countOfCaptainsPicked[captainName] = 1

            listOfcountOfPlayersPicked = sorted(countOfPlayersPicked.items(), key=lambda x: x[1], reverse=True)
            writeToFile(listOfcountOfPlayersPicked, "playersPicked-" + str(leagueIdSelected) + "-GW" + str(GWNumber) + ".csv")
            listOfCountOfCaptainsPicked = sorted(countOfCaptainsPicked.items(), key=lambda x: x[1], reverse=True)
            writeToFile(listOfCountOfCaptainsPicked, "captain-" + str(leagueIdSelected) + "-GW" + str(GWNumber) + ".csv")
            pageCount += 1
            return True
        except Exception as e: # TODO: Give a more specific Error?
            print('Error while getting the data' ,e)
            return False


# Writes the results to csv file
def writeToFile(countOfPlayersPicked, fileName):
    fullPath = f"{PACKAGE_DIR}/results/{fileName}"
    with open(fullPath, 'w') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['name', 'num'])
        for row in countOfPlayersPicked:
            csv_out.writerow(row)

# Main Script
def main(): 
    parser = argparse.ArgumentParser(description='Get players picked in your league in a certain GameWeek')
    parser.add_argument('-g','--gameweek', help='gameweek number', required=True)
    parser.add_argument('-t', '--type', help='league type')
    args = vars(parser.parse_args())

    pageCount = START_PAGE
    GWNumber = args['gameweek']
    leagueIdSelected = os.environ['LEAGUE_ID']

    if args['type'] == "h2h":
        leagueStandingUrl = FPL_URL + LEAGUE_H2H_STANDING_SUBURL
    else:
        leagueStandingUrl = FPL_URL + LEAGUE_CLASSIC_STANDING_SUBURL

    
    # collate all the player and captain picks in in a single csv file 
    getPlayerAndCaptainNumbers(leagueIdSelected, pageCount, leagueStandingUrl, GWNumber)


if __name__ == "__main__":
    main()