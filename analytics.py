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
    """Read the sales CSV and return it with dates and amounts properly typed."""
    df = pd.read_csv(Path(path))
    df["date"] = pd.to_datetime(df["date"])
    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column])
    return df
