import os
from config.constants import (
    RAW_DATA_DIR, FORMATTED_DATA_DIR, DEFAULT_LOOKBACK_DAYS,
    SAVE_TO_DRIVE, GOOGLE_DRIVE_FOLDER_ID
)
from services.slack_client import fetch_messages, save_raw_data
from services.formatter import parse_for_rag
from services.drive_uploader import upload_to_drive


def run(days=DEFAULT_LOOKBACK_DAYS):
    messages = fetch_messages(days)

    raw_file = os.path.join(RAW_DATA_DIR, "slack_raw.json")
    formatted_file = os.path.join(FORMATTED_DATA_DIR, "slack_rag.json")

    save_raw_data(messages, raw_file)
    parse_for_rag(raw_file, formatted_file)

    if SAVE_TO_DRIVE:
        upload_to_drive(raw_file, GOOGLE_DRIVE_FOLDER_ID)
        upload_to_drive(formatted_file, GOOGLE_DRIVE_FOLDER_ID)


if __name__ == "__main__":
    run()
