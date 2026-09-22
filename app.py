"""ShopSmart Sales Dashboard.

The only module in this project that imports Streamlit. Loading, calculation, and
chart construction live in analytics.py and charts.py so they stay testable.
"""

from pathlib import Path

import streamlit as st

import analytics
import charts

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

sales_column, orders_column = st.columns(2)
sales_column.metric("Total Sales", analytics.format_currency(analytics.total_sales(df)))
orders_column.metric("Total Orders", analytics.format_count(analytics.total_orders(df)))

st.subheader("Sales Trend Over Time")
st.plotly_chart(charts.trend_chart(analytics.sales_by_week(df)), width="stretch")

category_column, region_column = st.columns(2)

with category_column:
    st.subheader("Sales by Category")
    st.plotly_chart(
        charts.category_chart(analytics.sales_by_category(df)),
        width="stretch",
    )

with region_column:
    st.subheader("Sales by Region")
    st.plotly_chart(
        charts.region_chart(analytics.sales_by_region(df)),
        width="stretch",
    )
