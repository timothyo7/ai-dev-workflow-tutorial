"""Structural smoke tests for charts.py.

These do not judge how a chart looks — that is checked by running the app. They
catch typos and wiring mistakes in pytest instead of in the browser.
"""

import analytics
import charts
from test_analytics import sample_df


def test_trend_chart_returns_one_line_trace():
    figure = charts.trend_chart(analytics.sales_by_week(sample_df()))
    assert len(figure.data) == 1


def test_trend_chart_labels_both_axes():
    figure = charts.trend_chart(analytics.sales_by_week(sample_df()))
    assert figure.layout.xaxis.title.text
    assert figure.layout.yaxis.title.text


def test_category_chart_has_one_horizontal_bar_trace():
    figure = charts.category_chart(analytics.sales_by_category(sample_df()))
    assert len(figure.data) == 1
    assert figure.data[0].orientation == "h"


def test_region_chart_has_one_horizontal_bar_trace():
    figure = charts.region_chart(analytics.sales_by_region(sample_df()))
    assert len(figure.data) == 1
    assert figure.data[0].orientation == "h"


def test_bar_charts_put_the_largest_value_on_top():
    figure = charts.category_chart(analytics.sales_by_category(sample_df()))
    # Horizontal bars render bottom-up, so ascending order puts the biggest at top.
    assert figure.layout.yaxis.categoryorder == "total ascending"


def test_trend_chart_hovertemplate_shows_exact_value_in_dollars():
    figure = charts.trend_chart(analytics.sales_by_week(sample_df()))
    template = figure.data[0].hovertemplate
    assert "%{y" in template
    assert "$" in template


def test_category_chart_hovertemplate_shows_exact_value_in_dollars():
    figure = charts.category_chart(analytics.sales_by_category(sample_df()))
    template = figure.data[0].hovertemplate
    assert "%{x" in template
    assert "$" in template


def test_region_chart_hovertemplate_shows_exact_value_in_dollars():
    figure = charts.region_chart(analytics.sales_by_region(sample_df()))
    template = figure.data[0].hovertemplate
    assert "%{x" in template
    assert "$" in template
