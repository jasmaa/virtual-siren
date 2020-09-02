import os
import subprocess as sp
from dotenv import load_dotenv

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

sp.run(command)
