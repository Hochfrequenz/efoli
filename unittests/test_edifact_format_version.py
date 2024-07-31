from datetime import datetime, timezone

import pytest

from efoli import EdifactFormatVersion, get_current_edifact_format_version, get_edifact_format_version


@pytest.mark.parametrize(
    "key_date,expected_result",
    [
        pytest.param(
            datetime(2021, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
            EdifactFormatVersion.FV2104,
            id="Anything before 2021-04-01",
        ),
        pytest.param(datetime(2021, 5, 1, 0, 0, 0, tzinfo=timezone.utc), EdifactFormatVersion.FV2104),
        pytest.param(datetime(2021, 10, 1, 0, 0, 0, tzinfo=timezone.utc), EdifactFormatVersion.FV2110),
        pytest.param(datetime(2022, 7, 1, 0, 0, 0, tzinfo=timezone.utc), EdifactFormatVersion.FV2110),
        pytest.param(datetime(2022, 10, 1, 0, 0, 0, tzinfo=timezone.utc), EdifactFormatVersion.FV2210),
        pytest.param(datetime(2022, 10, 1, 0, 0, 0, tzinfo=timezone.utc), EdifactFormatVersion.FV2210),
        pytest.param(datetime(2023, 12, 1, 0, 0, 0, tzinfo=timezone.utc), EdifactFormatVersion.FV2310),
        pytest.param(datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc), EdifactFormatVersion.FV2310),
        pytest.param(
            datetime(2024, 4, 1, 0, 0, 0, tzinfo=timezone.utc), EdifactFormatVersion.FV2310
        ),  # 2404 is valid form 2024-04-03 onwards
        pytest.param(datetime(2024, 4, 2, 22, 0, 0, tzinfo=timezone.utc), EdifactFormatVersion.FV2404),
        pytest.param(datetime(2024, 9, 30, 21, 59, 59, tzinfo=timezone.utc), EdifactFormatVersion.FV2404),
        pytest.param(datetime(2024, 9, 30, 22, 0, 0, 0, tzinfo=timezone.utc), EdifactFormatVersion.FV2410),
        pytest.param(datetime(2025, 3, 31, 22, 0, 0, tzinfo=timezone.utc), EdifactFormatVersion.FV2410),
        pytest.param(datetime(2025, 4, 3, 22, 0, 0, tzinfo=timezone.utc), EdifactFormatVersion.FV2504),
        pytest.param(datetime(2025, 9, 30, 22, 0, 0, tzinfo=timezone.utc), EdifactFormatVersion.FV2510),
        pytest.param(
            datetime(2050, 10, 1, 0, 0, 0, tzinfo=timezone.utc), EdifactFormatVersion.FV2510
        ),  # or what ever is the latest version
    ],
)
def test_format_version_from_keydate(key_date: datetime, expected_result: EdifactFormatVersion) -> None:
    actual = get_edifact_format_version(key_date)
    assert actual == expected_result


def test_get_current_format_version() -> None:
    actual = get_current_edifact_format_version()
    assert isinstance(actual, EdifactFormatVersion) is True
