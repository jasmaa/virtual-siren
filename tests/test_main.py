import os
import unittest
import datetime
from unittest.mock import patch
import main

TEST_ENV_VARS = {
    "RTMP_URL": "rtmp://rtmp.example.com",
    "STREAM_KEY": "test_stream_key",
    "INPUT_FILE": "https://storage.example.com/siren.mp4",
    "TZ": "America/New_York",
    "MSTDN_ACCESS_TOKEN": "test_access_token",
    "MSTDN_URL": "https://mstdn.example.com",
    "STREAM_URL": "https://twitch.example.com",
}


@patch.dict(os.environ, TEST_ENV_VARS)
class TestMain(unittest.TestCase):

    @patch('subprocess.run')
    @patch('requests.post')
    @patch('main.get_today')
    def test_should_stream_siren_when_first_wednesday_of_month(self, get_today, post, run):
        get_today.return_value = datetime.datetime(2023, 7, 5)
        run.return_value = None
        post.return_value = {}

        main.stream_siren({})

        post.assert_called_once()
        run.assert_called_once()

    @patch('subprocess.run')
    @patch('requests.post')
    @patch('main.get_today')
    def test_should_not_stream_siren_when_not_first_wednesday_of_month(self, get_today, post, run):
        get_today.return_value = datetime.datetime(2023, 7, 4)
        run.return_value = None
        post.return_value = {}

        main.stream_siren({})

        post.assert_not_called()
        run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
