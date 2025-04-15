# slack-scraper-bot

Bot that scrapes messages (including threads) from a Slack channel and saves the conversations in a format optimized for
Retrieval-Augmented Generation (RAG) pipelines. Optionally, the bot can also upload the data to a specified Google Drive
folder.

## Features

- Fetch messages and threads from a Slack channel
- Format messages into a structured format suitable for LLMs
- Upload raw and formatted data to Google Drive

## Project Structure

```
slack-scraper-bot/
├── config/
│   └── constants.py                 # Configuration variables
├── data/
│   ├── raw/                         # Raw Slack messages
│   └── formatted/                   # Formatted RAG-ready data
├── services/
│   ├── slack_client.py              # Slack API logic
│   ├── formatter.py                 # Data formatting logic
│   ├── s3_uploader.py               # Upload logic for S3
│   └── drive_uploader.py            # Upload logic for Google Drive
├── utils/
│   └── time_utils.py                # Time related util functions
├── main.py                          # Entry point
├── .env                             # Secrets and tokens
├── .gitignore
└── README.md
```

## Environment Variables

Create a `.env` file in the root directory and define the following:

| Variable Name            | Description                                                                     |
|--------------------------|---------------------------------------------------------------------------------|
| `SLACK_BOT_TOKEN`        | **(Required)** Slack Bot token to authenticate API calls                        |
| `SLACK_CHANNEL_ID`       | **(Optional)** Channel ID if known; if empty, it will be fetched using the name |
| `GOOGLE_DRIVE_FOLDER_ID` | **(Required if SAVE_TO_DRIVE=True)** Folder ID to upload files in Google Drive  |
| `GOOGLE_DRIVE_CRED_LINK` | Path to the Google credentials JSON (defaults to `credentials.json`)            |
| `AWS_ACCESS_KEY_ID`      | **(Required for S3 integration)** AWS access key for S3 authentication         |
| `AWS_SECRET_ACCESS_KEY`  | **(Required for S3 integration)** AWS secret key for S3 authentication         |
| `AWS_REGION`             | **(Required for S3 integration)** AWS region for the S3 bucket                 |
| `S3_BUCKET_NAME`         | **(Required for S3 integration)** S3 bucket name where files will be uploaded |
| `S3_PREFIX`              | **(Optional)** Prefix for organizing files in S3 bucket                        |

### Sample `.env` file

```env
SLACK_BOT_TOKEN=xoxb-your-token-here
SLACK_CHANNEL_ID=C123456xxxx
GOOGLE_DRIVE_FOLDER_ID=1ABcdefxxxxxxxx
GOOGLE_DRIVE_CRED_LINK=credentials.json
AWS_ACCESS_KEY_ID=your-aws-access-key-id
AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
AWS_REGION=your-aws-region
S3_BUCKET_NAME=your-s3-bucket-name
S3_PREFIX=your-s3-prefix
```

## Sample Formatted Data (RAG-ready)

Each formatted Slack thread will look like the following JSON structure:

```json
{
  "thread_ts": "1712819200.123456",
  "date": "2025-04-12",
  "slack_link": "https://slack.com/archives/C01S8CY1P0T/p1712819200123456",
  "context": "Description:\nDevRev Ticket ISS-1234 has been raised.\nuser1: Please check logs\nuser2: Acknowledged and will investigate."
}
```

- `thread_ts`: The original timestamp of the Slack thread
- `date`: Date of the base message
- `slack_link`: Direct Slack link to the thread
- `context`: Complete context combining description and follow-up messages in a readable format, ready for RAG ingestion
