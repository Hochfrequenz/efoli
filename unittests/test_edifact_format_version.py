from datetime import date, datetime, timezone

import pytest

from efoli import (
    EdifactFormatVersion,
    get_current_edifact_format_version,
    get_edifact_format_version,
    get_edifact_format_version_valid_from,
)


@pytest.mark.parametrize(
    "key_date,expected_result",
    [
        pytest.param(
            datetime(2021, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
            EdifactFormatVersion.FV2104,
            id="Anything before 2021-04-01 (datetime)",
        ),
        pytest.param(
            date(2021, 1, 1),
            EdifactFormatVersion.FV2104,
            id="Anything before 2021-04-01 (date)",
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
        pytest.param(datetime(2025, 4, 3, 22, 0, 0, tzinfo=timezone.utc), EdifactFormatVersion.FV2410),
        pytest.param(datetime(2025, 6, 5, 22, 0, 0, tzinfo=timezone.utc), EdifactFormatVersion.FV2504),
        pytest.param(date(2025, 4, 3), EdifactFormatVersion.FV2410),
        pytest.param(date(2025, 4, 4), EdifactFormatVersion.FV2410),
        pytest.param(date(2025, 6, 6), EdifactFormatVersion.FV2504),
        pytest.param(datetime(2025, 9, 30, 22, 0, 0, tzinfo=timezone.utc), EdifactFormatVersion.FV2510),
        pytest.param(datetime(2025, 10, 1, 22, 0, 0, tzinfo=timezone.utc), EdifactFormatVersion.FV2510),
        pytest.param(datetime(2026, 3, 31, 21, 59, 59, tzinfo=timezone.utc), EdifactFormatVersion.FV2510),
        pytest.param(datetime(2026, 3, 31, 22, 0, 0, tzinfo=timezone.utc), EdifactFormatVersion.FV2604),
        pytest.param(datetime(2026, 9, 30, 22, 0, 0, tzinfo=timezone.utc), EdifactFormatVersion.FV2610),
        pytest.param(
            datetime(2050, 10, 1, 0, 0, 0, tzinfo=timezone.utc), EdifactFormatVersion.FV2610
        ),  # or what ever is the latest version
    ],
)
def test_format_version_from_keydate(key_date: datetime, expected_result: EdifactFormatVersion) -> None:
    actual = get_edifact_format_version(key_date)
    assert actual == expected_result


def test_get_current_format_version() -> None:
    actual = get_current_edifact_format_version()
    assert isinstance(actual, EdifactFormatVersion) is True


def test_str_representation() -> None:
    assert str(EdifactFormatVersion.FV2504) == "FV2504"


@pytest.mark.parametrize(
    "version,expected_date",
    [
        pytest.param(EdifactFormatVersion.FV2110, date(2021, 10, 1), id="FV2110"),
        pytest.param(EdifactFormatVersion.FV2210, date(2022, 10, 1), id="FV2210"),
        pytest.param(EdifactFormatVersion.FV2304, date(2023, 4, 1), id="FV2304"),
        pytest.param(EdifactFormatVersion.FV2310, date(2023, 10, 1), id="FV2310"),
        pytest.param(EdifactFormatVersion.FV2404, date(2024, 4, 3), id="FV2404"),
        pytest.param(EdifactFormatVersion.FV2410, date(2024, 10, 1), id="FV2410"),
        pytest.param(EdifactFormatVersion.FV2504, date(2025, 6, 6), id="FV2504"),
        pytest.param(EdifactFormatVersion.FV2510, date(2025, 10, 1), id="FV2510"),
        pytest.param(EdifactFormatVersion.FV2604, date(2026, 4, 1), id="FV2604"),
        pytest.param(EdifactFormatVersion.FV2610, date(2026, 10, 1), id="FV2610"),
    ],
)
def test_format_version_valid_from(version: EdifactFormatVersion, expected_date: date) -> None:
    actual = get_edifact_format_version_valid_from(version)
    assert actual == expected_date


def test_format_version_valid_from_unknown_raises() -> None:
    with pytest.raises(KeyError):
        get_edifact_format_version_valid_from(EdifactFormatVersion.FV2104)


def test_all_format_versions_except_first_have_valid_from() -> None:
    """Every FV except the very first (FV2104) must have a known start date.
    This test fails if a new FV is added to the enum but not to the thresholds list."""
    all_fvs = list(EdifactFormatVersion)
    first_fv = all_fvs[0]
    for fv in all_fvs[1:]:
        result = get_edifact_format_version_valid_from(fv)
        assert isinstance(result, date), f"{fv} should have a valid_from date"
    # First FV has no start date
    with pytest.raises(KeyError):
        get_edifact_format_version_valid_from(first_fv)
