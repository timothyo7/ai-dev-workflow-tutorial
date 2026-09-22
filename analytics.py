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

# Columns used as groupby keys by the breakdown charts. pandas.groupby drops
# null keys by default, so a blank value here would quietly remove the row from
# a chart while leaving it in the Total Sales KPI -- the two would disagree with
# no error shown. They are validated for exactly that reason.
GROUPING_COLUMNS = ["category", "region"]


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

    for column in GROUPING_COLUMNS:
        _reject_blank(df, column)

    original_dates = df["date"]
    df["date"] = pd.to_datetime(original_dates, errors="coerce")
    _reject_unparsed(df, df["date"], original_dates, "date", "a valid date")

    for column in NUMERIC_COLUMNS:
        original = df[column]
        df[column] = pd.to_numeric(original, errors="coerce")
        _reject_unparsed(df, df[column], original, column, "a number")

    return df


def _reject_unparsed(df, coerced, original, column, expectation):
    """Raise DataError if coercion left any NaN, quoting the first bad value."""
    unparsed = coerced.isna()
    if not unparsed.any():
        return
    position = int(unparsed.to_numpy().argmax())
    raise DataError(
        f"Column '{column}' contains a value that is not {expectation}: "
        f"{_describe(original.iloc[position])} ({_identify_row(df, position)})."
    )


def _reject_blank(df, column):
    """Raise DataError if any row has no usable value in a grouping column."""
    blank = df[column].map(_is_blank)
    if not blank.any():
        return
    position = int(blank.to_numpy().argmax())
    raise DataError(
        f"Column '{column}' is empty for at least one row "
        f"({_identify_row(df, position)}). Every row needs a {column} so the "
        f"breakdown charts add up to the same total as the KPI."
    )


def _is_blank(value):
    """True for NaN and for strings that are empty or only whitespace."""
    return pd.isna(value) or not str(value).strip()


def _describe(value):
    """Render a cell for an error message, without pretending NaN is text."""
    return "an empty value" if _is_blank(value) else repr(str(value))


def _identify_row(df, position):
    """Point at a row by order_id.

    Deliberately not a file line number: pandas skips blank lines and folds
    quoted newlines into a single row, so row position and file line drift
    apart and the number would send the reader to the wrong row.
    """
    order_id = df["order_id"].iloc[position]
    if _is_blank(order_id):
        return f"data row {position + 1}"
    return f"order_id {order_id}"


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


def sales_by_week(df):
    """Total sales per calendar week, oldest first.

    Weeks are labelled by their start date rather than a week number so the
    chart plots on a real time axis and tooltips read as dates.
    """
    if df.empty:
        return pd.DataFrame({"week_start": [], "total_amount": []})

    week_start = df["date"].dt.to_period("W").dt.start_time
    return (
        df.assign(week_start=week_start)
        .groupby("week_start", as_index=False)["total_amount"]
        .sum()
        .sort_values("week_start")
        .reset_index(drop=True)
    )


def _sales_grouped_by(df, column):
    """Sum total_amount per value of `column`, biggest first."""
    if df.empty:
        return pd.DataFrame({column: [], "total_amount": []})

    return (
        df.groupby(column, as_index=False)["total_amount"]
        .sum()
        .sort_values("total_amount", ascending=False)
        .reset_index(drop=True)
    )


def sales_by_category(df):
    """Total sales per product category, highest first."""
    return _sales_grouped_by(df, "category")


def sales_by_region(df):
    """Total sales per geographic region, highest first."""
    return _sales_grouped_by(df, "region")
