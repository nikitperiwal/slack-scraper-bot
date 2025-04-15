import os
import argparse
from datetime import datetime, timedelta

from config.constants import (
    RAW_DATA_DIR, FORMATTED_DATA_DIR, SAVE_TO_DRIVE, GOOGLE_DRIVE_FOLDER_ID, SAVE_TO_S3, S3_BUCKET_NAME, S3_PREFIX
)
from services import slack_client
from services import formatter
from services.drive_uploader import upload_folder_to_drive
from services.s3_uploader import upload_folder_to_s3


def run_batch(days=1, batch_size=1):
    today = datetime.now()

    for i in range(0, days, batch_size):
        end_day = today - timedelta(days=i)
        start_day = end_day - timedelta(days=batch_size)

        start_ts = int(start_day.timestamp())
        end_ts = int(end_day.timestamp())

        date_str = start_day.strftime("%Y-%m-%d")
        print(f"\nFetching batch: {date_str} | From {start_day} to {end_day}")

        # Fetch Slack messages for this window
        messages = slack_client.fetch_messages_from_threads(start_ts, end_ts)
        if not messages:
            print(f"No messages found for {date_str}")
            continue

        # Save raw data
        raw_file = os.path.join(RAW_DATA_DIR, f"slack_{date_str}.json")

        slack_client.save_raw_data(messages, raw_file)
        formatter.parse_for_rag(RAW_DATA_DIR, FORMATTED_DATA_DIR)

        if SAVE_TO_DRIVE:
            upload_folder_to_drive(FORMATTED_DATA_DIR, GOOGLE_DRIVE_FOLDER_ID)

        if SAVE_TO_S3:
            upload_folder_to_s3(FORMATTED_DATA_DIR, S3_BUCKET_NAME, S3_PREFIX)


if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Scrape Slack data for RAG processing.")
    parser.add_argument('--days', type=int, default=1, help="Number of days to fetch messages for.")
    parser.add_argument('--batch_size', type=int, default=1, help="Batch size for the fetch.")

    args = parser.parse_args()

    # Run the batch process with provided arguments
    run_batch(days=args.days, batch_size=args.batch_size)
