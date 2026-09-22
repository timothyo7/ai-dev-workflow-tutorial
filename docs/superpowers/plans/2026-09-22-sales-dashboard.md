# ShopSmart Sales Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the Phase 1 ShopSmart sales dashboard — two KPIs, a weekly sales trend line, and category and region breakdowns — as a Streamlit app reading `data/sales-data.csv`.

**Architecture:** Three modules with a hard boundary: `analytics.py` (pure pandas: load, validate, aggregate, format) and `charts.py` (pure Plotly figure builders) import no Streamlit at all, so pytest exercises them directly. `app.py` is the only Streamlit importer and wraps `analytics.load_data` in a thin `@st.cache_data` function.

**Tech Stack:** Python 3.14 (local), Streamlit, Pandas, Plotly, pytest. Plain `venv/` + `requirements.txt`.

**Spec:** `docs/superpowers/specs/2026-09-22-sales-dashboard-design.md`

## Numbering Convention

This plan's own units are **Step 1 … Step 9**. The milestone each step serves is
written in parentheses as **(TASK-n)**, matching `TASKS.md`. The two schemes are
independent — never renumber one to match the other.

## Global Constraints

Every step's requirements implicitly include all of these:

- Work on branch `feature/sales-dashboard`. Do **not** create a git worktree. Do **not** touch `main`.
- Virtual environment is a plain `venv/` created with `python3 -m venv`. No uv, no conda, no poetry.
- Dependencies are declared in `requirements.txt`. `venv/` is already covered by `.gitignore`.
- `analytics.py` and `charts.py` must **never** import `streamlit`. `app.py` is the only file that may.
- Keep code simple and readable: plain functions, no classes beyond the one `DataError` exception, comments where the *why* is not obvious.
- Every commit message includes its milestone ID, e.g. `TASK-3`, per the Definition of Done in `TASKS.md`.
- Required CSV columns, exact spelling: `date`, `order_id`, `product`, `category`, `region`, `quantity`, `unit_price`, `total_amount`.
- Known-good values for `data/sales-data.csv`: total sales `116500.21`, 482 rows, 482 distinct `order_id`, 5 categories, 4 regions, top category Electronics.
- Do not build anything in the PRD's Phase 2 list (auth, database, export, alerts, filtering, drill-down, mobile). Not even stubbed.
- After each step, move the milestone in `TASKS.md` and tick its acceptance criteria when the step completes that milestone.

---

### Step 1: Environment setup and skeleton (TASK-1)

Front-loaded deliberately: the only interpreter on this machine is Python 3.14.7, and
some wheels may not publish for it yet. Find out now, before any code exists.

**Files:**
- Create: `requirements.txt`
- Create: `app.py`
- Create: `conftest.py`

- [ ] **Step 1.1: Confirm the branch**

```bash
git rev-parse --abbrev-ref HEAD
```

Expected: `feature/sales-dashboard`. If not, stop and ask — do not switch branches unprompted.

- [ ] **Step 1.2: Create and activate the virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate
python -V
```

Expected: a `venv/` directory and `Python 3.14.7`.

- [ ] **Step 1.3: Install dependencies**

```bash
python -m pip install --upgrade pip
python -m pip install streamlit pandas plotly pytest
```

Expected: all four install cleanly.

**If any package has no wheel for 3.14 and fails to build:** stop and report it. Do not
switch to conda or uv (Global Constraints). The fallback is installing a 3.13 interpreter
via Homebrew (`brew install python@3.13`) and recreating the venv with
`python3.13 -m venv venv` — but that is the user's call, so ask first.

- [ ] **Step 1.4: Pin the installed versions**

```bash
python -m pip freeze | grep -iE '^(streamlit|pandas|plotly|pytest)==' | sort > requirements.txt
cat requirements.txt
```

Expected: four `name==version` lines.

Note: spec §7 says "pinned to minor versions". Exact `==` pins from `pip freeze` are
strictly stronger and are what Streamlit Community Cloud reproduces most reliably. This
is a deliberate refinement of the spec, recorded here rather than made silently.

- [ ] **Step 1.5: Create the root conftest.py**

pytest inserts the *test file's* directory on `sys.path`, not the project root — so
`tests/test_analytics.py` could not `import analytics` without this. An empty `conftest.py`
at the root makes pytest add the root to `sys.path`.

```python
# Present so pytest adds the project root to sys.path, letting tests
# import analytics.py and charts.py from the repository root.
```

Save that single comment line as `conftest.py`.

- [ ] **Step 1.6: Create the placeholder app**

```python
"""ShopSmart Sales Dashboard."""

import streamlit as st

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")

st.title("ShopSmart Sales Dashboard")
st.write("Dashboard under construction.")
```

- [ ] **Step 1.7: Verify the app runs**

```bash
streamlit run app.py
```

Expected: a browser tab showing the title and the placeholder line, and **no warnings**
in the terminal. Record the Streamlit version printed by `python -m pip show streamlit`;
Step 8 needs it. Stop the server with Ctrl-C.

- [ ] **Step 1.8: Commit**

```bash
git add requirements.txt app.py conftest.py
git commit -m "TASK-1: set up venv, dependencies, and app skeleton"
```

- [ ] **Step 1.9: Update TASKS.md**

Tick TASK-1's three criteria, fill its `**Commit:**` line with the short SHA from
`git rev-parse --short HEAD`, and move the whole TASK-1 block to the `## Done` section.

```bash
git add TASKS.md && git commit -m "TASK-1: mark milestone done"
```

---

### Step 2: Data loading (TASK-2)

**Files:**
- Create: `analytics.py`
- Create: `tests/test_analytics.py`

**Interfaces:**
- Consumes: nothing from earlier steps.
- Produces:
  - `DataError(Exception)`
  - `REQUIRED_COLUMNS: list[str]`
  - `load_data(path: str | Path) -> pd.DataFrame` — `date` as datetime64, `quantity`/`unit_price`/`total_amount` numeric

- [ ] **Step 2.1: Write the failing tests**

Create `tests/test_analytics.py`:

```python
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
```

- [ ] **Step 2.2: Run the tests to verify they fail**

```bash
pytest tests/test_analytics.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'analytics'`.

- [ ] **Step 2.3: Write the minimal implementation**

Create `analytics.py`:

```python
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
```

- [ ] **Step 2.4: Run the tests to verify they pass**

```bash
pytest tests/test_analytics.py -v
```

Expected: 4 passed.

- [ ] **Step 2.5: Commit**

```bash
git add analytics.py tests/test_analytics.py
git commit -m "TASK-2: load and type sales CSV with tests"
```

---

### Step 3: Validation and error messages (TASK-6)

Validation is built now, immediately after loading, so that no later step is written
against an unguarded loader. Fail fast with one clear message (spec D4).

**Files:**
- Modify: `analytics.py` (replace the body of `load_data`)
- Modify: `tests/test_analytics.py` (append)

**Interfaces:**
- Consumes: `DataError`, `REQUIRED_COLUMNS`, `NUMERIC_COLUMNS`, `load_data` from Step 2.
- Produces: `load_data` now raises `DataError` with a human-readable message on every failure mode. No signature change.

- [ ] **Step 3.1: Write the failing tests**

Append to `tests/test_analytics.py`:

```python
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
```

- [ ] **Step 3.2: Run the tests to verify they fail**

```bash
pytest tests/test_analytics.py -v
```

Expected: the five new tests FAIL — the current `load_data` raises `FileNotFoundError`,
`KeyError`, or `ValueError` rather than `DataError`.

- [ ] **Step 3.3: Write the implementation**

Replace `load_data` in `analytics.py` with:

```python
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
```

- [ ] **Step 3.4: Run the tests to verify they pass**

```bash
pytest tests/test_analytics.py -v
```

Expected: 9 passed.

- [ ] **Step 3.5: Commit**

```bash
git add analytics.py tests/test_analytics.py
git commit -m "TASK-6: validate CSV and fail fast with clear messages"
```

Move the TASK-6 block in `TASKS.md` from `## To Do` to `## In Progress` and tick its
first two criteria. Its third criterion ("no warnings") is confirmed in Step 8, so it
stays in `## In Progress` until then.

```bash
git add TASKS.md && git commit -m "TASK-6: move milestone to in progress"
```

---

### Step 4: App shell with cached loading and error path (TASK-2, TASK-6)

**Files:**
- Modify: `app.py` (full rewrite)

**Interfaces:**
- Consumes: `analytics.load_data`, `analytics.DataError` from Steps 2–3.
- Produces: `get_data(path) -> pd.DataFrame`, a `@st.cache_data`-wrapped loader; the module-level `df` every later step renders from.

- [ ] **Step 4.1: Rewrite app.py**

```python
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
```

- [ ] **Step 4.2: Verify the happy path**

```bash
streamlit run app.py
```

Expected: the title plus `482 transactions loaded from sales-data.csv`. No warnings in
the terminal.

- [ ] **Step 4.3: Verify the error path**

With the app still running, temporarily rename the data file and let Streamlit rerun:

```bash
mv data/sales-data.csv data/sales-data.csv.bak
```

Expected: a red error box reading "Could not load sales data." with the "not found"
message, and **no** caption or partial dashboard below it. Then restore it:

```bash
mv data/sales-data.csv.bak data/sales-data.csv
```

Confirm the dashboard returns. Stop the server.

- [ ] **Step 4.4: Commit**

```bash
git add app.py
git commit -m "TASK-2: add cached data loading and TASK-6 error path to app"
```

- [ ] **Step 4.5: Update TASKS.md**

Tick TASK-2's criteria and move it to `## Done` with its commit SHA. Leave TASK-6 in
`## In Progress` — its "no warnings" criterion is confirmed in Step 8.

```bash
git add TASKS.md && git commit -m "TASK-2: mark milestone done"
```

---

### Step 5: KPI cards (TASK-3)

**Files:**
- Modify: `analytics.py` (append)
- Modify: `tests/test_analytics.py` (append)
- Modify: `app.py` (append)

**Interfaces:**
- Consumes: `load_data` from Steps 2–3; `df` from Step 4.
- Produces:
  - `total_sales(df) -> float`
  - `total_orders(df) -> int`
  - `format_currency(value) -> str` — `116500.21` → `"$116,500"`
  - `format_count(value) -> str` — `482` → `"482"`
  - `sample_df()` test helper in `tests/test_analytics.py`

- [ ] **Step 5.1: Write the failing tests**

Append to `tests/test_analytics.py`:

```python
def sample_df():
    """Six rows whose totals are checkable by hand: they sum to 300.00.

    Two dates fall in the same ISO week (2024-01-01 and 2024-01-03) so weekly
    bucketing has something real to collapse.
    """
    return pd.DataFrame(
        {
            "date": pd.to_datetime(
                [
                    "2024-01-01",
                    "2024-01-03",
                    "2024-01-08",
                    "2024-01-15",
                    "2024-01-22",
                    "2024-01-29",
                ]
            ),
            "order_id": ["ORD-1", "ORD-2", "ORD-3", "ORD-4", "ORD-5", "ORD-6"],
            "product": ["A", "B", "C", "D", "E", "F"],
            "category": ["Audio", "Audio", "Wearables", "Audio", "Wearables", "Smart Home"],
            "region": ["North", "South", "North", "North", "South", "East"],
            "quantity": [1, 1, 1, 1, 1, 1],
            "unit_price": [100.0, 50.0, 40.0, 60.0, 30.0, 20.0],
            "total_amount": [100.0, 50.0, 40.0, 60.0, 30.0, 20.0],
        }
    )


def test_total_sales_sums_amounts():
    assert analytics.total_sales(sample_df()) == 300.00


def test_total_orders_counts_rows():
    assert analytics.total_orders(sample_df()) == 6


def test_total_sales_of_real_csv_matches_known_value():
    df = analytics.load_data(REAL_CSV)
    assert round(analytics.total_sales(df), 2) == 116500.21


def test_total_orders_of_real_csv_matches_known_value():
    df = analytics.load_data(REAL_CSV)
    assert analytics.total_orders(df) == 482


def test_every_row_is_a_distinct_order():
    # total_orders counts rows; this guards the assumption that lets it.
    df = analytics.load_data(REAL_CSV)
    assert df["order_id"].nunique() == analytics.total_orders(df)


def test_format_currency_rounds_and_separates():
    assert analytics.format_currency(116500.21) == "$116,500"


def test_format_count_separates_thousands():
    assert analytics.format_count(482) == "482"
    assert analytics.format_count(12345) == "12,345"
```

- [ ] **Step 5.2: Run the tests to verify they fail**

```bash
pytest tests/test_analytics.py -v
```

Expected: the seven new tests FAIL with `AttributeError: module 'analytics' has no
attribute 'total_sales'` and similar.

- [ ] **Step 5.3: Write the implementation**

Append to `analytics.py`:

```python
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
```

- [ ] **Step 5.4: Run the tests to verify they pass**

```bash
pytest tests/test_analytics.py -v
```

Expected: 16 passed.

- [ ] **Step 5.5: Render the KPI row**

Append to `app.py`, replacing the `st.caption(...)` line from Step 4:

```python
sales_column, orders_column = st.columns(2)
sales_column.metric("Total Sales", analytics.format_currency(analytics.total_sales(df)))
orders_column.metric("Total Orders", analytics.format_count(analytics.total_orders(df)))
```

- [ ] **Step 5.6: Verify in the browser**

```bash
streamlit run app.py
```

Expected: two metrics side by side reading `$116,500` and `482`. Stop the server.

- [ ] **Step 5.7: Commit and update TASKS.md**

```bash
git add analytics.py tests/test_analytics.py app.py
git commit -m "TASK-3: add total sales and orders KPI cards"
```

Tick TASK-3's criteria, record the SHA, move it to `## Done`, then:

```bash
git add TASKS.md && git commit -m "TASK-3: mark milestone done"
```

---

### Step 6: Sales trend chart (TASK-4)

**Files:**
- Modify: `analytics.py` (append)
- Create: `charts.py`
- Modify: `tests/test_analytics.py` (append)
- Create: `tests/test_charts.py`
- Modify: `app.py` (append)

**Interfaces:**
- Consumes: `sample_df()`, `load_data`, `df` from earlier steps.
- Produces:
  - `analytics.sales_by_week(df) -> pd.DataFrame` with columns `week_start` (datetime64) and `total_amount` (float), ascending by week
  - `charts.PALETTE: list[str]`
  - `charts.trend_chart(weekly) -> plotly.graph_objects.Figure`

- [ ] **Step 6.1: Write the failing aggregation tests**

Append to `tests/test_analytics.py`:

```python
def test_sales_by_week_collapses_dates_in_the_same_week():
    weekly = analytics.sales_by_week(sample_df())
    # 2024-01-01 and 2024-01-03 share an ISO week, so six rows become five.
    assert len(weekly) == 5
    assert weekly.iloc[0]["total_amount"] == 150.0


def test_sales_by_week_is_sorted_ascending():
    weekly = analytics.sales_by_week(sample_df())
    assert list(weekly["week_start"]) == sorted(weekly["week_start"])


def test_sales_by_week_totals_match_overall_total():
    df = analytics.load_data(REAL_CSV)
    weekly = analytics.sales_by_week(df)
    assert round(weekly["total_amount"].sum(), 2) == 116500.21


def test_sales_by_week_handles_empty_data():
    empty = sample_df().iloc[0:0]
    weekly = analytics.sales_by_week(empty)
    assert len(weekly) == 0
```

- [ ] **Step 6.2: Run to verify they fail**

```bash
pytest tests/test_analytics.py -v
```

Expected: the four new tests FAIL with `AttributeError: ... has no attribute 'sales_by_week'`.

- [ ] **Step 6.3: Implement the aggregation**

Append to `analytics.py`:

```python
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
```

- [ ] **Step 6.4: Run to verify they pass**

```bash
pytest tests/test_analytics.py -v
```

Expected: 20 passed.

- [ ] **Step 6.5: Write the failing chart test**

Create `tests/test_charts.py`:

```python
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
```

If `from tests.test_analytics import sample_df` fails to resolve, add an empty
`tests/__init__.py` and re-run. Do not duplicate `sample_df` into this file.

- [ ] **Step 6.6: Run to verify it fails**

```bash
pytest tests/test_charts.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'charts'`.

- [ ] **Step 6.7: Implement charts.py**

```python
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
```

- [ ] **Step 6.8: Run to verify it passes**

```bash
pytest -v
```

Expected: 22 passed.

- [ ] **Step 6.9: Render the trend chart**

Add to `app.py` — the import goes at the top beside `import analytics`, the rest below
the KPI row:

```python
import charts
```

```python
st.subheader("Sales Trend Over Time")
st.plotly_chart(charts.trend_chart(analytics.sales_by_week(df)), use_container_width=True)
```

- [ ] **Step 6.10: Verify in the browser**

```bash
streamlit run app.py
```

Expected: a line chart with roughly 52 points spanning Jan–Dec 2024, hovering shows
`Week of Mar 04, 2024 / Sales: $3,214`-style tooltips. Note whether the terminal prints
any deprecation warning about `use_container_width` — Step 8 resolves it. Stop the server.

- [ ] **Step 6.11: Commit and update TASKS.md**

```bash
git add analytics.py charts.py tests/ app.py
git commit -m "TASK-4: add weekly sales trend chart"
```

Tick TASK-4's criteria, record the SHA, move to `## Done`, then:

```bash
git add TASKS.md && git commit -m "TASK-4: mark milestone done"
```

---

### Step 7: Category and region breakdowns (TASK-5)

**Files:**
- Modify: `analytics.py` (append)
- Modify: `charts.py` (append)
- Modify: `tests/test_analytics.py` (append)
- Modify: `tests/test_charts.py` (append)
- Modify: `app.py` (append)

**Interfaces:**
- Consumes: everything from Steps 2–6.
- Produces:
  - `analytics.sales_by_category(df) -> pd.DataFrame[category, total_amount]`, descending
  - `analytics.sales_by_region(df) -> pd.DataFrame[region, total_amount]`, descending
  - `charts.category_chart(by_category) -> Figure`
  - `charts.region_chart(by_region) -> Figure`

- [ ] **Step 7.1: Write the failing aggregation tests**

Append to `tests/test_analytics.py`:

```python
def test_sales_by_category_sorted_highest_first():
    result = analytics.sales_by_category(sample_df())
    # Audio 100+50+60 = 210, Wearables 40+30 = 70, Smart Home 20
    assert list(result["category"]) == ["Audio", "Wearables", "Smart Home"]
    assert list(result["total_amount"]) == [210.0, 70.0, 20.0]


def test_sales_by_region_sorted_highest_first():
    result = analytics.sales_by_region(sample_df())
    # North 100+40+60 = 200, South 50+30 = 80, East 20
    assert list(result["region"]) == ["North", "South", "East"]


def test_sales_by_category_handles_ties():
    tied = pd.DataFrame(
        {"category": ["A", "B"], "total_amount": [50.0, 50.0]}
    )
    result = analytics.sales_by_category(tied)
    assert len(result) == 2
    assert set(result["category"]) == {"A", "B"}


def test_real_csv_has_five_categories_led_by_electronics():
    df = analytics.load_data(REAL_CSV)
    result = analytics.sales_by_category(df)
    assert len(result) == 5
    assert result.iloc[0]["category"] == "Electronics"


def test_real_csv_has_four_regions():
    df = analytics.load_data(REAL_CSV)
    result = analytics.sales_by_region(df)
    assert len(result) == 4
    assert set(result["region"]) == {"North", "South", "East", "West"}


def test_breakdown_totals_match_overall_total():
    df = analytics.load_data(REAL_CSV)
    assert round(analytics.sales_by_category(df)["total_amount"].sum(), 2) == 116500.21
    assert round(analytics.sales_by_region(df)["total_amount"].sum(), 2) == 116500.21


def test_breakdowns_handle_empty_data():
    empty = sample_df().iloc[0:0]
    assert len(analytics.sales_by_category(empty)) == 0
    assert len(analytics.sales_by_region(empty)) == 0
```

- [ ] **Step 7.2: Run to verify they fail**

```bash
pytest tests/test_analytics.py -v
```

Expected: FAIL — no attribute `sales_by_category`.

- [ ] **Step 7.3: Implement the aggregations**

Append to `analytics.py`:

```python
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
```

- [ ] **Step 7.4: Run to verify they pass**

```bash
pytest tests/test_analytics.py -v
```

Expected: 27 passed.

- [ ] **Step 7.5: Write the failing chart tests**

Append to `tests/test_charts.py`:

```python
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
```

- [ ] **Step 7.6: Run to verify they fail**

```bash
pytest tests/test_charts.py -v
```

Expected: FAIL — no attribute `category_chart`.

- [ ] **Step 7.7: Implement the bar charts**

Append to `charts.py`:

```python
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
```

- [ ] **Step 7.8: Run the full suite**

```bash
pytest -v
```

Expected: 32 passed.

- [ ] **Step 7.9: Render the two-column breakdown row**

Append to `app.py`:

```python
category_column, region_column = st.columns(2)

with category_column:
    st.subheader("Sales by Category")
    st.plotly_chart(
        charts.category_chart(analytics.sales_by_category(df)),
        use_container_width=True,
    )

with region_column:
    st.subheader("Sales by Region")
    st.plotly_chart(
        charts.region_chart(analytics.sales_by_region(df)),
        use_container_width=True,
    )
```

- [ ] **Step 7.10: Verify in the browser**

```bash
streamlit run app.py
```

Expected: two side-by-side bar charts; Electronics is the top bar on the left, all 5
categories and all 4 regions present, tooltips show exact dollar values. Stop the server.

- [ ] **Step 7.11: Commit and update TASKS.md**

```bash
git add analytics.py charts.py tests/ app.py
git commit -m "TASK-5: add category and region breakdown charts"
```

Tick TASK-5's criteria, record the SHA, move to `## Done`, then:

```bash
git add TASKS.md && git commit -m "TASK-5: mark milestone done"
```

---

### Step 8: Theme, warning sweep, and refinement (TASK-6, TASK-7)

**Files:**
- Create: `.streamlit/config.toml`
- Modify: `app.py` (only if the deprecation check in 8.2 requires it)
- Modify: `README.md`

**Interfaces:**
- Consumes: the complete app from Steps 1–7.
- Produces: no new callable interfaces. Closes out TASK-6's "no warnings" criterion and all of TASK-7.

- [ ] **Step 8.1: Add the theme config**

Create `.streamlit/config.toml`:

```toml
# Theme only — no custom CSS. CSS that targets Streamlit's internal class names
# breaks silently across versions; a theme block is supported API.
[theme]
primaryColor = "#2563eb"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f8fafc"
textColor = "#0f172a"
font = "sans serif"
```

Note `.streamlit/secrets.toml` is gitignored but `config.toml` is not — that is correct,
the theme must ship to Streamlit Cloud.

- [ ] **Step 8.2: Sweep for deprecation warnings**

```bash
streamlit run app.py
```

Read the terminal output carefully. Streamlit deprecated `use_container_width` in favour
of `width` in recent versions. **If** you see a deprecation warning naming it, replace
every occurrence in `app.py`:

```python
# before
st.plotly_chart(figure, use_container_width=True)

# after
st.plotly_chart(figure, width="stretch")
```

There are three call sites: the trend chart and the two breakdown charts. If no warning
appears, change nothing — the installed version still prefers the old argument.

- [ ] **Step 8.3: Confirm a clean run**

Restart the app and confirm the terminal shows **zero** warnings from Streamlit or Pandas
and the browser console shows no errors (open DevTools with Cmd-Option-I).

This closes TASK-6's third criterion.

- [ ] **Step 8.4: Check load time**

Reload the page and time it. Expected: well under the PRD's 5-second budget — the dataset
is 482 rows and `get_data` is cached after the first load. If it exceeds 5 seconds,
report it rather than optimising speculatively.

- [ ] **Step 8.5: Cross-browser check**

Open the same `localhost` URL in a second browser (Safari and Chrome, or Chrome and
Firefox). Confirm KPIs, all three charts, and tooltips render in both. This closes
TASK-7's third criterion.

- [ ] **Step 8.6: Read the code once, end to end**

Open `analytics.py`, `charts.py`, and `app.py` in order and confirm:

- No `import streamlit` in `analytics.py` or `charts.py`
- Every public function has a one-line docstring
- No leftover debugging code, commented-out blocks, or unused imports
- No Phase 2 features crept in

```bash
grep -n "streamlit" analytics.py charts.py
```

Expected: no matches at all.

- [ ] **Step 8.7: Run the full suite one more time**

```bash
pytest -v
```

Expected: 32 passed, no warnings.

- [ ] **Step 8.8: Add run instructions to README.md**

Append to `README.md`:

````markdown
## Sales Dashboard

Local setup:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Run the tests with `pytest`.

**Live dashboard:** _(deployed URL goes here — see TASK-8)_
````

- [ ] **Step 8.9: Commit and update TASKS.md**

```bash
git add .streamlit/config.toml app.py README.md
git commit -m "TASK-7: add theme, clear warnings, document local setup (closes TASK-6)"
```

Tick the remaining criteria on TASK-6 and TASK-7, record SHAs, move both to `## Done`,
then:

```bash
git add TASKS.md && git commit -m "TASK-6 TASK-7: mark milestones done"
```

---

### Step 9: Deployment handoff (TASK-8) — USER-EXECUTED

> **This step is the user's to perform. The implementation plan stops at the end of
> Step 8 with `feature/sales-dashboard` merge-ready. Do not merge, do not push, do not
> modify `main`, and do not deploy. If you are an agent executing this plan, stop after
> Step 8 and hand back.**

The remaining work, for the user:

- [ ] **Step 9.1: Review and merge**

Review the branch, then merge to `main` locally and push.

- [ ] **Step 9.2: Push the repo to GitHub**

Streamlit Community Cloud deploys from a GitHub repository, so `main` must exist on
GitHub with `app.py`, `requirements.txt`, `.streamlit/config.toml`, and `data/sales-data.csv`
committed. `venv/` must stay untracked.

- [ ] **Step 9.3: Deploy**

At share.streamlit.io, create a new app pointing at the repo, branch `main`, main file
`app.py`.

**Watch the Python version selector.** This machine only has Python 3.14, but Streamlit
Community Cloud may not offer 3.14 in its list. Nothing in this codebase uses 3.14-only
syntax, so selecting **3.13** (or whatever the highest offered version is) is safe and
expected.

- [ ] **Step 9.4: Verify the deployed app**

Open the public URL and confirm: both KPIs show `$116,500` and `482`, the trend chart
spans Jan–Dec 2024, and both breakdown charts render with Electronics on top.

- [ ] **Step 9.5: Record the URL**

Replace the `_(deployed URL goes here — see TASK-8)_` placeholder in `README.md` with the
real URL, tick TASK-8's criteria in `TASKS.md`, move it to `## Done`, and commit:

```bash
git commit -am "TASK-8: record deployed dashboard URL"
```
