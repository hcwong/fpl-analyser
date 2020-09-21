import unittest
from unittest.mock import Mock, patch

from fplanalyzer.definitions import MIN_GAMEWEEK, MAX_GAMEWEEK
from fplanalyzer.fplrequests import getPlayerAndCaptainNumbers
from fplanalyzer.fpl_api import is_gameweek_valid, get_current_gameweek, get_league_users

class TestFPLApi(unittest.TestCase):
    def test_get_current_gameweek(self):
        with patch('fplanalyzer.fpl_api.requests.get') as mock_get:
            data = {"events": [
                {
                    "id": 2,
                    "is_current": True
                },
                {
                    "id": 1,
                    "is_current": False
                }
            ]}
            mock_get.return_value.ok = True
            mock_get.return_value.json.return_value = data

            response = get_current_gameweek()
        self.assertTrue(response == 2)

    @patch('fplanalyzer.fpl_api.requests.get')
    def test_is_gameweek_valid(self, mock_get):
        data = {"events": [
            {
                "id": 2,
                "is_current": True
            },
            {
                "id": 1,
                "is_current": False
            }
        ]}
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = data
        self.assertTrue(is_gameweek_valid(2))
        self.assertTrue(not is_gameweek_valid(3))

    @patch('fplanalyzer.fpl_api.requests.get')
    def test_get_league_users(self, mock_get):
        data = {"standings": {
            "results": [
                {
                    "id": 1,
                    "total": 23,
                    "entry": 333,
                    "entry_name": "team",
                    "player_name": "name"
                }
            ]
        }}
        mock_responses = [Mock(), Mock()]
        mock_responses[0].return_value.ok = True
        mock_responses[1].return_value.ok = False
        mock_responses[0].json.return_value = data
        mock_get.side_effect = mock_responses
        response = get_league_users(901)
        self.assertTrue(len(response) == 1)

        with self.assertRaises(Exception) as context:
            get_league_users(902)
        self.assertTrue("Could not get" in str(context.exception))



