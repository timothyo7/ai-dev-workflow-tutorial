"""ShopSmart Sales Dashboard.

The only module in this project that imports Streamlit. Loading, calculation, and
chart construction live in analytics.py and charts.py so they stay testable.
"""

from pathlib import Path

import streamlit as st

import analytics

DATA_PATH = Path(__file__).parent / "data" / "sales-data.csv"

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")


@st.cache_data
def get_data(path):
    """Load the sales data once and reuse it across reruns.

    Caching lives here rather than in analytics.py: that keeps the analytics
    module free of Streamlit so pytest can import it directly.
    """
    return analytics.load_data(path)


st.title("ShopSmart Sales Dashboard")

try:
    df = get_data(DATA_PATH)
except analytics.DataError as error:
    st.error(f"Could not load sales data.\n\n{error}")
    st.stop()

st.caption(f"{len(df):,} transactions loaded from {DATA_PATH.name}")
