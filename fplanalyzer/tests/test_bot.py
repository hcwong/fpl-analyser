import unittest
from unittest.mock import Mock, patch

from bot import get_rankings_over_last_gameweeks

class Chat:
    def __init__(self):
        self.id = 1

class Bot:
    def send_message(*args, **kwargs):
        pass

class MockUpdate:
    def __init__(self):
        self.effective_chat = Chat()

class MockContext:
    def __init__(self, args):
        self.args = args
        self.bot = Bot()

class TestBot(unittest.TestCase):
    @patch('fplanalyzer.fpl_api.requests.get')
    def test_get_rankings_over_last_gameweeks(self, mock_get):
        dates = {"events": [
            {
                "id": 2,
                "is_current": True
            },
            {
                "id": 1,
                "is_current": False
            }
        ]}

        users = {"standings": {
            "results": [
                {
                    "id": 1,
                    "total": 23,
                    "entry": 333,
                    "entry_name": "team",
                    "player_name": "name"
                },
                {
                    "id": 2,
                    "total": 23,
                    "entry": 334,
                    "entry_name": "team1",
                    "player_name": "name1"
                }
            ]
        }}

        gws = {
            "current": [
                {
                    "event": 1,
                    "points": 20,
                    "event_transfers_cost": 0
                }
            ]
        }

        gws2 = {
            "current": [
                {
                    "event": 1,
                    "points": 22,
                    "event_transfers_cost": 0
                }
            ]
        }

        mock_responses = [Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()]
        for m in mock_responses:
            m.return_value.ok = True
        mock_responses[0].json.return_value = users
        mock_responses[1].json.return_value = dates
        mock_responses[2].json.return_value = dates
        mock_responses[3].json.return_value = gws
        mock_responses[4].json.return_value = dates
        mock_responses[5].json.return_value = dates
        mock_responses[6].json.return_value = gws2
        mock_get.side_effect = mock_responses

        context = MockContext(['1','2'])
        update = MockUpdate()
        get_rankings_over_last_gameweeks(update, context)
        self.assertTrue(mock_get.call_count == 7)

