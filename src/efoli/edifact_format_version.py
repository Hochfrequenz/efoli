"""contains the EdifactFormatVersion enum"""

import datetime
from typing import Union

import pytz

from .strenum import StrEnum

_berlin = pytz.timezone("Europe/Berlin")


class EdifactFormatVersion(StrEnum):
    """
    One format version refers to the period in which an AHB is valid.
    """

    FV2104 = "FV2104"  #: valid from 2021-04-01 until 2021-10-01
    FV2110 = "FV2110"  #: valid from 2021-10-01 until 2022-04-01
    FV2210 = "FV2210"  #: valid from 2022-10-01 onwards ("MaKo 2022", was 2204 previously)
    FV2304 = "FV2304"  #: valid from 2023-04-01 onwards
    FV2310 = "FV2310"  #: valid from 2023-10-01 onwards
    FV2404 = "FV2404"  #: valid from 2024-04-01 onwards
    FV2410 = "FV2410"  #: valid from 2024-10-01 onwards
    FV2504 = "FV2504"  #: valid from 2025-04-04 onwards
    FV2510 = "FV2510"  #: valid from 2025-10-01 onwards
    # whenever you add another value here, please also make sure to add its key date to get_edifact_format_version below

    def __str__(self) -> str:
        return self.value


def get_edifact_format_version(key_date: Union[datetime.datetime, datetime.date]) -> EdifactFormatVersion:
    """
    Retrieves the appropriate Edifact format version applicable for the given key date.

    This function determines the correct Edifact format version by comparing the provided key date
    against a series of predefined datetime thresholds. Each threshold corresponds to a specific
    version of the Edifact format.

    :param key_date: The date for which the Edifact format version is to be determined.
    :return: The Edifact format version valid for the specified key date.
    """
    if not isinstance(key_date, datetime.datetime) and isinstance(key_date, datetime.date):
        key_date = _berlin.localize(datetime.datetime.combine(key_date, datetime.time(0, 0, 0, 0)))
    format_version_thresholds = [
        (datetime.datetime(2021, 9, 30, 22, 0, 0, 0, tzinfo=datetime.timezone.utc), EdifactFormatVersion.FV2104),
        (datetime.datetime(2022, 9, 30, 22, 0, 0, 0, tzinfo=datetime.timezone.utc), EdifactFormatVersion.FV2110),
        (datetime.datetime(2023, 3, 31, 22, 0, 0, 0, tzinfo=datetime.timezone.utc), EdifactFormatVersion.FV2210),
        (datetime.datetime(2023, 9, 30, 22, 0, 0, 0, tzinfo=datetime.timezone.utc), EdifactFormatVersion.FV2304),
        (datetime.datetime(2024, 4, 2, 22, 0, 0, 0, tzinfo=datetime.timezone.utc), EdifactFormatVersion.FV2310),
        (datetime.datetime(2024, 9, 30, 22, 0, 0, 0, tzinfo=datetime.timezone.utc), EdifactFormatVersion.FV2404),
        (datetime.datetime(2025, 4, 3, 22, 0, 0, 0, tzinfo=datetime.timezone.utc), EdifactFormatVersion.FV2410),
        (datetime.datetime(2025, 9, 30, 22, 0, 0, 0, tzinfo=datetime.timezone.utc), EdifactFormatVersion.FV2504),
    ]

    for threshold_date, version in format_version_thresholds:
        if key_date < threshold_date:
            return version

    return EdifactFormatVersion.FV2510


def get_current_edifact_format_version() -> EdifactFormatVersion:
    """
    returns the edifact_format_version that is valid as of now
    """
    tz_aware_now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    return get_edifact_format_version(tz_aware_now)
