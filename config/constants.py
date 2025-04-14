import os
from dotenv import load_dotenv

load_dotenv()

# Secrets from .env
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID", "")
GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "")

# Static config (safe to keep in repo)
SLACK_CHANNEL_NAME = "#data_platform_support"
DEFAULT_LOOKBACK_DAYS = 30
SAVE_TO_DRIVE = True

RAW_DATA_DIR = "data/raw"
FORMATTED_DATA_DIR = "data/formatted"
