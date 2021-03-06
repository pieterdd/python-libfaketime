import datetime

from pytest import raises
from pytz import timezone

from libfaketime import fake_time


def test_timezone_is_restored_after_context_manager_usage():
    """https://github.com/simon-weber/python-libfaketime/issues/43"""
    now1 = datetime.datetime.now()
    utcnow1 = datetime.datetime.utcnow()

    with fake_time(now1):
        datetime.datetime.now()

    now2 = datetime.datetime.now()
    utcnow2 = datetime.datetime.utcnow()

    assert abs((now2 - now1).total_seconds()) < 10
    assert abs((utcnow2 - utcnow1).total_seconds()) < 10


def test_tzinfo_is_normalized():
    """Ensure utcnow() behaves correctly when faking non-UTC timestamps."""
    timezone_to_test_with = timezone('Europe/Brussels')
    time_to_freeze = timezone_to_test_with.localize(datetime.datetime(2017, 1, 2, 15, 2))

    with fake_time(time_to_freeze):
        # The timeshift of Europe/Brussels is UTC+1 in January
        assert datetime.datetime.now() == datetime.datetime(2017, 1, 2, 15, 2)
        assert datetime.datetime.utcnow() == datetime.datetime(2017, 1, 2, 14, 2)


def test_block_setting_of_conflicting_tz_info():
    """Cannot pass in tz_offset when the timestamp already carries a timezone."""
    with raises(Exception) as exc_info:
        timezone_to_test_with = timezone('America/Havana')
        time_to_freeze = timezone_to_test_with.localize(datetime.datetime(2012, 10, 2, 21, 38))

        with fake_time(time_to_freeze, tz_offset=5):
            pass

    assert str(exc_info.value) == 'Cannot set tz_offset when datetime already has timezone'
