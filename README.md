# Virtual Tornado Siren

Google Cloud function to stream a video of a tornado siren to Twitch on the first Wednesday of every month at 11:55AM.

## Setup

### Pre-requisites:
  - Twitch account
  - Twitter account
  - GCP account

### Setup Twitch and Twitter
  - Setup Twitch streaming
    - Find your Twitch stream key (`STREAM KEY`) and appropriate [RTMP server](https://stream.twitch.tv/ingests/) (`RTMP_URL`)
    - Retrieve your Twitch account's URL. This will be `STREAM_URL`.
  - Setup Twitter reminder
    - Create a developer account on Twitter and retrieve your `TWITTER_API_KEY` and `TWITTER_API_SECRET`
    - Generate access token with read and write permissions and retrieve the `TWITTER_ACCESS_TOKEN` and `TWITTER_ACCESS_TOKEN_SECRET`

### Deploying to GCloud

Create a service user with `Cloud Function Invoker` privileges.

Find an `mp4` video of a tornado siren of your choosing and host it as publically viewable on a static storage solution
(Google Cloud Storage is one option). The path of the `mp4` will be `INPUT_FILE`.

Create a `.env.yaml` with and populate it with proper credentials.

Deploy and schedule the function with:

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