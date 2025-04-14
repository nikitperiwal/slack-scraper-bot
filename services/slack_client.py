import os
import json

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from config.constants import SLACK_BOT_TOKEN, SLACK_CHANNEL_ID, SLACK_CHANNEL_NAME

client = WebClient(token=SLACK_BOT_TOKEN)


def get_channel_id(channel_name):
    cursor = None
    while True:
        response = client.conversations_list(
            types="public_channel",
            limit=1000,  # max allowed by Slack
            cursor=cursor
        )
        channels = response.get("channels", [])
        for ch in channels:
            if ch["name"] == channel_name.strip("#"):
                return ch["id"]

        cursor = response.get("response_metadata", {}).get("next_cursor")
        if not cursor:
            break

    raise ValueError(f"Channel {channel_name} not found")


def fetch_messages_from_threads(oldest, latest):
    channel_id = SLACK_CHANNEL_ID or get_channel_id(SLACK_CHANNEL_NAME)

    messages = []
    cursor = None

    try:
        while True:
            response = client.conversations_history(
                channel=channel_id,
                oldest=oldest,
                latest=latest,
                limit=1000,  # Max allowed
                cursor=cursor
            )

            for msg in response["messages"]:
                if "thread_ts" in msg:
                    thread = client.conversations_replies(channel=channel_id, ts=msg["ts"])
                    messages.append(thread["messages"])
                else:
                    messages.append([msg])

            cursor = response.get("response_metadata", {}).get("next_cursor")
            if not cursor:
                break

    except SlackApiError as e:
        print(f"Error fetching messages: {e.response['error']}")

    return messages


def save_raw_data(messages, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(messages, f, indent=2)
