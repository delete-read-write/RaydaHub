import datetime as dt

import pytest

from raydahub.core.value_objects import DateTime


def test_datetime_converts_value_to_utc() -> None:
    moscow = dt.timezone(dt.timedelta(hours=3))

    sut = DateTime(dt.datetime(2026, 1, 1, 12, tzinfo=moscow))

    assert sut.value == dt.datetime(2026, 1, 1, 9, tzinfo=dt.UTC)
    assert sut.value.tzinfo is dt.UTC


def test_datetime_rejects_naive_value() -> None:
    naive = dt.datetime.now(dt.UTC).replace(tzinfo=None)

    with pytest.raises(ValueError, match="Naive datetime"):
        DateTime(naive)
