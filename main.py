import os
import urllib.parse
import sys
from datetime import datetime
import subprocess as sp
import logging
import requests
import pytz


def get_today():
    # Set timezone
    try:
        tz = pytz.timezone(os.getenv('TZ'))
    except pytz.exceptions.UnknownTimeZoneError:
        tz = pytz.timezone('UTC')

    today = datetime.today().astimezone(tz)
    return today


def stream_siren(request):
    """Streams siren video to Twitch
    """
    RTMP_URL = os.getenv('RTMP_URL')
    STREAM_KEY = os.getenv('STREAM_KEY')
    INPUT_FILE = os.getenv('INPUT_FILE')

    MSTDN_ACCESS_TOKEN = os.getenv('MSTDN_ACCESS_TOKEN')
    MSTDN_URL = os.getenv('MSTDN_URL')
    STREAM_URL = os.getenv('STREAM_URL')

    # Setup logger
    log = logging.getLogger(__name__)
    out_hdlr = logging.StreamHandler(sys.stdout)
    out_hdlr.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))
    out_hdlr.setLevel(logging.INFO)
    log.addHandler(out_hdlr)
    log.setLevel(logging.INFO)

    # Check if first Wednesday of the month
    today = get_today()
    if today.weekday() == 2 and today.day <= 7:
        # Toot reminder
        log.info('Tooting reminder...')
        try:
            date_str = today.strftime('%b %d, %Y')
            msg = f'Virtual siren for {date_str} has started at {STREAM_URL}!'
            requests.post(
                urllib.parse.urljoin(MSTDN_URL, "/api/v1/statuses"),
                headers={
                    "Authorization": f"Bearer {MSTDN_ACCESS_TOKEN}",
                }, data={
                    "status": msg,
                },
            )
        except Exception:
            log.warning('Could not send toot.')

        # FFMPEG stream to RTMP server
        log.info('Starting stream...')
        sp.run([
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
        ])
