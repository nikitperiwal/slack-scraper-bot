import json
import os

def parse_for_rag(input_file, output_file):
    with open(input_file, "r") as f:
        raw_data = json.load(f)

    parsed = []
    for thread in raw_data:
        joined_text = "\n".join([msg.get("text", "") for msg in thread])
        parsed.append({
            "thread_ts": thread[0]["ts"],
            "context": joined_text
        })

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(parsed, f, indent=2)
