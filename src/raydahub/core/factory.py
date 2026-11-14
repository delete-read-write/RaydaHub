import datetime as dt

from raydahub.core.value_objects import DateTime


def make_utc_now() -> DateTime:
    return DateTime(dt.datetime.now(dt.UTC))
