from datetime import datetime, timezone


def get_aware_datetime_now() -> datetime:
    datetime_now_aware_utc = datetime.now(timezone.utc)
    return datetime_now_aware_utc.replace(tzinfo=None)
