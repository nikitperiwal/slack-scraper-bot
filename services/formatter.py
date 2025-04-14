import json
import os
from datetime import datetime
from config.constants import SLACK_CHANNEL_ID


def parse_for_rag(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    all_files = [f for f in os.listdir(input_dir) if f.endswith(".json")]

    if not all_files:
        print(f"No .json files found in {input_dir}")
        return

    for file_name in all_files:
        input_file = os.path.join(input_dir, file_name)
        output_file = os.path.join(output_dir, file_name)

        with open(input_file, "r") as f:
            raw_data = json.load(f)

        print(f"Parsing {len(raw_data)} threads in {file_name}...")

        parsed = []
        for thread in raw_data:
            if not thread:
                continue

            base = thread[0]
            description = base.get("text", "").strip()
            date = datetime.fromtimestamp(float(base["ts"])).strftime("%Y-%m-%d")
            thread_ts = base["ts"]
            slack_link = f"https://slack.com/archives/{SLACK_CHANNEL_ID}/p{thread_ts.replace('.', '')}"

            chat_lines = []
            for msg in thread[1:]:
                user = msg.get("user", "Unknown")
                text = msg.get("text", "").strip()
                if text:
                    chat_lines.append(f"{user}: {text}")

            context = f"{description}\n <<Conversation Thread>>:" + "\n".join(chat_lines)

            parsed.append({
                "thread_ts": thread_ts,
                "date": date,
                "slack_link": slack_link,
                "context": context
            })

        with open(output_file, "w") as f:
            json.dump(parsed, f, indent=2)

        print(f"Saved {len(parsed)} threads to {output_file}")

