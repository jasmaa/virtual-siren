import os
import time
from datetime import datetime
import subprocess as sp
from dotenv import load_dotenv
import schedule

load_dotenv()

RTMP_URL = os.getenv('RTMP_URL')
STREAM_KEY = os.getenv('STREAM_KEY')
INPUT_FILE = os.getenv('INPUT_FILE')

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
    if datetime.today().weekday() == 2 and datetime.today().day <= 7: 
        print('Start stream...')
        sp.run(command)


if __name__ == '__main__':
    schedule.every().day.at('11:55').do(stream_siren)
    print('Start worker...')
    
    while True:
        schedule.run_pending()
        time.sleep(1)
