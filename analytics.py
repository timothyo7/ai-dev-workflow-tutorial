"""Data loading, validation, and aggregation for the ShopSmart sales dashboard.

This module imports no Streamlit on purpose: keeping it framework-free means the
numbers can be tested with plain pytest, and a wrong figure is always traceable
to this file rather than to the page that renders it.
"""

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = [
    "date",
    "order_id",
    "product",
    "category",
    "region",
    "quantity",
    "unit_price",
    "total_amount",
]

NUMERIC_COLUMNS = ["quantity", "unit_price", "total_amount"]


class DataError(Exception):
    """Raised when the sales CSV is missing, unreadable, or malformed."""


def load_data(path):
    """Read and validate the sales CSV.

    Validation is strict and fails on the first problem found. A dashboard that
    refuses to render and says why is safer than one showing a silently wrong
    total in an executive meeting.

    Raises:
        DataError: with a message naming the specific problem.
    """
    path = Path(path)

    if not path.exists():
        raise DataError(f"Sales data file not found: {path}")

    try:
        df = pd.read_csv(path)
    except Exception as exc:
        raise DataError(f"Could not read {path} as a CSV file: {exc}") from exc

    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise DataError(
            "Sales data is missing required column(s): "
            + ", ".join(missing)
            + ". Expected: "
            + ", ".join(REQUIRED_COLUMNS)
        )

    df = df.copy()

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    _reject_unparsed(df["date"], "date", "a valid date")

    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")
        _reject_unparsed(df[column], column, "a number")

    return df


def _reject_unparsed(series, column, expectation):
    """Raise DataError if coercion left any NaN, naming the first bad CSV line."""
    unparsed = series.isna()
    if not unparsed.any():
        return
    # +2 converts a zero-based row position into a 1-based CSV line number,
    # accounting for the header line.
    line = int(unparsed.to_numpy().argmax()) + 2
    raise DataError(
        f"Column '{column}' contains a value that is not {expectation} "
        f"(first problem on line {line} of the file)."
    )


def total_sales(df):
    """Sum of every transaction's total_amount."""
    return float(df["total_amount"].sum())


def total_orders(df):
    """Count of transactions.

    Row count is the order count: every order_id in the source data is unique,
    an invariant the test suite asserts.
    """
    return int(len(df))


def format_currency(value):
    """116500.21 -> '$116,500'."""
    return f"${value:,.0f}"


def format_count(value):
    """482 -> '482'; 12345 -> '12,345'."""
    return f"{value:,}"
