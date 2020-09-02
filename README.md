# Virtual Tornado Siren

Streams a video of a tornado siren to Twitch on the first Wednesday of every month at 11:55AM.

# Setup

Pre-requisites:
  - FFMPEG
  - Twitch account

Find an `mp4` video of a tornado siren of your choosing. Its path will be `INPUT_FILE`.

Find your Twitch stream key (`STREAM KEY`) and appropriate
[RTMP server](https://stream.twitch.tv/ingests/) (`RTMP_URL`)

Create a `.env` file at the repo root and populate it with proper environment variables.

Run:

    pip install -r requirements.txt
    python app.py