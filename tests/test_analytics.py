"""Tests for analytics.py — the data loading and aggregation module."""

import pandas as pd
import pytest

import analytics

REAL_CSV = "data/sales-data.csv"


def test_load_data_returns_all_rows():
    df = analytics.load_data(REAL_CSV)
    assert len(df) == 482


def test_load_data_parses_dates_as_datetimes():
    df = analytics.load_data(REAL_CSV)
    assert pd.api.types.is_datetime64_any_dtype(df["date"])


def test_load_data_parses_amounts_as_numbers():
    df = analytics.load_data(REAL_CSV)
    for column in ["quantity", "unit_price", "total_amount"]:
        assert pd.api.types.is_numeric_dtype(df[column])


def test_load_data_keeps_every_required_column():
    df = analytics.load_data(REAL_CSV)
    for column in analytics.REQUIRED_COLUMNS:
        assert column in df.columns


def write_csv(tmp_path, text):
    """Write a CSV to a temp dir and return its path."""
    path = tmp_path / "sales.csv"
    path.write_text(text)
    return path


GOOD_HEADER = (
    "date,order_id,product,category,region,quantity,unit_price,total_amount\n"
)
GOOD_ROW = "2024-01-03,ORD-1,Earbuds,Audio,North,2,79.99,159.98\n"


def test_missing_file_raises_data_error():
    with pytest.raises(analytics.DataError) as excinfo:
        analytics.load_data("data/does-not-exist.csv")
    assert "not found" in str(excinfo.value)


def test_missing_column_raises_data_error_naming_it(tmp_path):
    header = GOOD_HEADER.replace("region,", "")
    row = GOOD_ROW.replace("North,", "")
    path = write_csv(tmp_path, header + row)
    with pytest.raises(analytics.DataError) as excinfo:
        analytics.load_data(path)
    assert "region" in str(excinfo.value)


def test_unparseable_date_raises_data_error(tmp_path):
    bad_row = GOOD_ROW.replace("2024-01-03", "not-a-date")
    path = write_csv(tmp_path, GOOD_HEADER + bad_row)
    with pytest.raises(analytics.DataError) as excinfo:
        analytics.load_data(path)
    assert "date" in str(excinfo.value)


def test_unparseable_amount_raises_data_error(tmp_path):
    bad_row = GOOD_ROW.replace(",159.98", ",N/A")
    path = write_csv(tmp_path, GOOD_HEADER + bad_row)
    with pytest.raises(analytics.DataError) as excinfo:
        analytics.load_data(path)
    assert "total_amount" in str(excinfo.value)


def test_valid_file_still_loads(tmp_path):
    path = write_csv(tmp_path, GOOD_HEADER + GOOD_ROW)
    df = analytics.load_data(path)
    assert len(df) == 1
