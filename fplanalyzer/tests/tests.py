import unittest
import os

from dotenv import load_dotenv
load_dotenv()

from ..definitions import *
from ..fplrequests import getPlayerAndCaptainNumbers


class Test(unittest.TestCase):
    leagueIdSelected = os.environ['LEAGUE_ID']
    leagueStandingUrl = FPL_URL + LEAGUE_CLASSIC_STANDING_SUBURL
    pageCount = START_PAGE

    def testApiCallSuccess(self):
        self.assertTrue(getPlayerAndCaptainNumbers(self.leagueIdSelected, self.pageCount, self.leagueStandingUrl, 2))
     
if __name__ == '__main__':
    unittest.main()    