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
