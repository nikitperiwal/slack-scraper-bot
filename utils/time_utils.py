from datetime import datetime, timedelta

def get_unix_range_from_days(days):
    now = datetime.now()
    oldest = now - timedelta(days=days)
    return oldest.timestamp(), now.timestamp()
