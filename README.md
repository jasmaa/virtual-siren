# Virtual Tornado Siren

Google Cloud function to stream a video of a tornado siren to Twitch on the
first Wednesday of every month at 11:55AM.

## Setup

### Pre-requisites:
  - Twitch account
  - Mastodon account (optional)
  - GCP account (only if deploying to GCP)

### Setup Twitch and Mastodon
  - Setup Twitch streaming
    - Find your Twitch stream key (`STREAM KEY`) and appropriate [RTMP
      server](https://stream.twitch.tv/ingests/) (`RTMP_URL`)
    - Retrieve your Twitch account's URL. This will be `STREAM_URL`.
  - Setup Mastodon reminder (optional)
    - Create a bot account on Mastodon instance of your choice. The url of the
      instance will be `MSTDN_URL`.
    - Go to settings and create an application. This will generate an access
      token which will be `MSTDN_ACCESS_TOKEN`.

### Option 1: Deploy to Ubuntu

Ensure `ffmpeg` is installed on your machine:

```
sudo apt install ffmpeg
```

Clone the repo to your machine at `/opt`.

Install dependencies:

```
pip3 install -r requirements.txt
```

Find an `mp4` video of a tornado siren of your choosing and save it to your
machine (ex. `data/siren.mp4`). The path of the `mp4` will be `INPUT_FILE`.

Create `.env` from `sample.env` and fill with your values.

Schedule a cronjob:

```
sudo crontab -e
```

```
55 11 * * * cd /opt/virtual-siren && python3 main.py
```

### Option 2: Deploy to GCloud

Create a service user with `Cloud Function Invoker` privileges.

Find an `mp4` video of a tornado siren of your choosing and host it as
publically viewable on a static storage solution (Google Cloud Storage is one
option). The path of the `mp4` will be `INPUT_FILE`.

Create a `.env.yaml` with and populate it with proper credentials.

Deploy and schedule the function with:

```bash
# Deploy function
gcloud functions deploy stream_siren \
  --runtime python37 \
  --trigger-http \
  --region <REGION> \
  --env-vars-file .env.yaml \
  --timeout 240

# Create scheduled job
gcloud scheduler jobs create http stream-siren-job \
  --schedule "55 11 * * *" \
  --http-method GET \
  --time-zone "America/New_York" \
  --uri <TRIGGER URI> \
  --oidc-service-account-email <SERVICE ACCOUNT EMAIL>
```

## Testing

```
python -m unittest discover --verbose tests
```