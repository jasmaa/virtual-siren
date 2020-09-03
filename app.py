import os
import time
from datetime import datetime
import subprocess as sp
from dotenv import load_dotenv
import schedule
import tweepy

load_dotenv()

RTMP_URL = os.getenv('RTMP_URL')
STREAM_KEY = os.getenv('STREAM_KEY')
INPUT_FILE = os.getenv('INPUT_FILE')

TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
STREAM_URL = os.getenv('STREAM_URL')

auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

command = [
    'ffmpeg',
    '-re',
    '-i', INPUT_FILE,
    '-vcodec', 'libx264',
    '-profile:v', 'main',
    '-preset:v', 'medium',
    '-r', '30',
    '-g', '60',
    '-keyint_min', '60',
    '-sc_threshold', '0',
    '-b:v', '2500k',
    '-maxrate', '2500k',
    '-bufsize', '2500k',
    '-sws_flags', 'lanczos+accurate_rnd',
    '-b:a', '96k',
    '-ar', '48000',
    '-ac', '2',
    '-f', 'flv',
    os.path.join(RTMP_URL, STREAM_KEY),
]

def stream_siren():
    """Streams siren video to Twitch
    """
    # Check if first Wednesday of the month
    today = datetime.today()
    if today.weekday() == 2 and today.day <= 7:
        date_str = today.strftime('%b %d, %Y')
        api.update_status(f'Virtual siren for {date_str} has started at {STREAM_URL}!')
        print('Start stream...')
        sp.run(command)


if __name__ == '__main__':
    schedule.every().day.at('11:55').do(stream_siren)
    print('Start worker...')
    
    while True:
        schedule.run_pending()
        time.sleep(1)
