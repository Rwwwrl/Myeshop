from datetime import datetime

import pytz


def utc_now() -> datetime:
    return datetime.now(tz=pytz.UTC)
