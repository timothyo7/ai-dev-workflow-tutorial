"""Plotly figure builders for the ShopSmart dashboard.

Like analytics.py, this imports no Streamlit: a figure is just data, and keeping
it that way means a chart bug is reproducible in a test rather than only on screen.
Each builder takes an already-aggregated DataFrame — no calculation happens here.
"""

import plotly.express as px

# One palette shared by every figure so the dashboard reads as a single system.
PALETTE = ["#2563eb", "#60a5fa", "#1e40af", "#93c5fd", "#3b82f6"]


def _style(figure):
    """Apply the shared look: tight margins, soft gridlines, no redundant legend."""
    figure.update_layout(
        margin=dict(l=10, r=10, t=30, b=10),
        plot_bgcolor="white",
        showlegend=False,
        font=dict(size=13),
    )
    figure.update_xaxes(showgrid=False)
    figure.update_yaxes(gridcolor="#eef2f7")
    return figure


def trend_chart(weekly):
    """Line chart of weekly sales. Expects columns week_start and total_amount."""
    figure = px.line(
        weekly,
        x="week_start",
        y="total_amount",
        markers=True,
        color_discrete_sequence=PALETTE,
    )
    figure.update_traces(
        hovertemplate="Week of %{x|%b %d, %Y}<br>Sales: $%{y:,.0f}<extra></extra>"
    )
    figure.update_layout(xaxis_title="Week", yaxis_title="Sales")
    return _style(figure)


def _breakdown_chart(data, dimension):
    """Horizontal bar chart of total_amount by `dimension`, largest bar on top.

    Horizontal because labels like "Smart Home" and "Accessories" read cleanly
    on a vertical axis without rotating the text.
    """
    figure = px.bar(
        data,
        x="total_amount",
        y=dimension,
        orientation="h",
        color_discrete_sequence=PALETTE,
    )
    figure.update_traces(hovertemplate="%{y}<br>Sales: $%{x:,.0f}<extra></extra>")
    figure.update_layout(xaxis_title="Sales", yaxis_title="")
    figure.update_yaxes(categoryorder="total ascending")
    return _style(figure)


def category_chart(by_category):
    """Sales by product category. Expects columns category and total_amount."""
    return _breakdown_chart(by_category, "category")


def region_chart(by_region):
    """Sales by geographic region. Expects columns region and total_amount."""
    return _breakdown_chart(by_region, "region")
