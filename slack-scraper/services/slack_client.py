import os
import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from config.constants import SLACK_BOT_TOKEN, SLACK_CHANNEL_NAME
from utils.time_utils import get_unix_range_from_days

client = WebClient(token=SLACK_BOT_TOKEN)

def get_channel_id(channel_name):
    channels = client.conversations_list(types="public_channel,private_channel")["channels"]
    for ch in channels:
        if ch["name"] == channel_name.strip("#"):
            return ch["id"]
    raise ValueError(f"Channel {channel_name} not found")

def fetch_messages(days=30):
    channel_id = get_channel_id(SLACK_CHANNEL_NAME)
    oldest, latest = get_unix_range_from_days(days)

    messages = []
    try:
        response = client.conversations_history(channel=channel_id, oldest=oldest, latest=latest)
        for msg in response["messages"]:
            # Fetch thread replies if it's a thread
            if "thread_ts" in msg:
                thread = client.conversations_replies(channel=channel_id, ts=msg["ts"])
                messages.append(thread["messages"])
            else:
                messages.append([msg])
    except SlackApiError as e:
        print(f"Error fetching messages: {e.response['error']}")
    return messages

def save_raw_data(messages, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(messages, f, indent=2)
