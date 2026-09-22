"""Structural smoke tests for charts.py.

These do not judge how a chart looks — that is checked by running the app. They
catch typos and wiring mistakes in pytest instead of in the browser.
"""

import analytics
import charts
from tests.test_analytics import sample_df


def test_trend_chart_returns_one_line_trace():
    figure = charts.trend_chart(analytics.sales_by_week(sample_df()))
    assert len(figure.data) == 1


def test_trend_chart_labels_both_axes():
    figure = charts.trend_chart(analytics.sales_by_week(sample_df()))
    assert figure.layout.xaxis.title.text
    assert figure.layout.yaxis.title.text
