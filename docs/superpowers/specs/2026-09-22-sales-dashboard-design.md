# Design: ShopSmart Sales Dashboard

**Date:** 2026-09-22
**Status:** Approved for planning
**Source PRD:** `prd/ecommerce-analytics.md`
**Milestone tracker:** `TASKS.md`
**Branch:** `feature/sales-dashboard`

---

## 1. Purpose and Scope

Build the Phase 1 sales dashboard described in the PRD: a Streamlit application that reads
`data/sales-data.csv` and presents two KPIs, a sales trend line chart, and category and region
breakdowns.

### In scope

- FR-1 KPI display (Total Sales, Total Orders)
- FR-2 Sales trend visualization
- FR-3 Category breakdown
- FR-4 Regional breakdown
- FR-5 CSV data source with validation
- NFR-1 through NFR-5

### Out of scope

Everything the PRD lists under Phase 2: authentication, database integration, export, alerts,
filtering and date-range selection, drill-down, mobile-responsive design. The PRD names scope creep
as a High-impact risk; these are not built, not stubbed, and not designed for.

---

## 2. Decisions

These were settled during brainstorming and are the reason the design looks the way it does.

| # | Decision | Rationale |
|---|----------|-----------|
| D1 | Trend chart uses **weekly** granularity | 482 transactions over 365 days averages ~1.3 orders/day, so a daily line is dominated by single-order spikes. Weekly gives 52 points: responsive enough to show movement, smooth enough to read. |
| D2 | Weekly buckets are **week-start dates**, not `W13` labels | Real timestamps sort correctly, render on a true time axis, and produce readable tooltips ("Week of Mar 4"). String labels do none of these. |
| D3 | **Three modules**: `app.py`, `analytics.py`, `charts.py` | Separates "is the math right" (pytest) from "does it look right" (visual check) from "is the page laid out right". Each file stays small enough to hold in your head. |
| D4 | Validation **fails fast** with one clear message | The PRD's goal is a single source of truth. A silently wrong KPI in an executive meeting is worse than a dashboard that refuses to render and says why. |
| D5 | Tests use **hand-checkable fixtures plus real-CSV assertions** | Fixtures make expected values verifiable by eye and allow edge cases; real-CSV tests guard against the shipped data file drifting from the PRD's expected numbers. |
| D6 | Styling is a **theme config plus a shared palette**, no custom CSS | Achieves "professional appearance" without CSS that targets Streamlit's internal class names, which change between versions and break silently. |
| D7 | Plain `venv/` and `requirements.txt` | User constraint: no uv, no conda. `venv/` is already covered by `.gitignore`. |
| D8 | Work on `feature/sales-dashboard`, no git worktree | User constraint. |

---

## 3. Architecture

```
data/sales-data.csv
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│ analytics.py            pure pandas + stdlib            │
│                         NO streamlit import             │
│   DataError                custom exception             │
│   load_data(path)          read, validate, coerce       │
│   total_sales(df)          float                        │
│   total_orders(df)         int                          │
│   sales_by_week(df)        DataFrame[week_start, total] │
│   sales_by_category(df)    DataFrame, sorted desc       │
│   sales_by_region(df)      DataFrame, sorted desc       │
│   format_currency(value)   116500.21 -> "$116,500"      │
│   format_count(value)      482 -> "482"                 │
└─────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│ charts.py               pure plotly                     │
│                         NO streamlit import             │
│   PALETTE                  shared color sequence        │
│   trend_chart(weekly)      -> go.Figure                 │
│   category_chart(cats)     -> go.Figure                 │
│   region_chart(regions)    -> go.Figure                 │
└─────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│ app.py                  the ONLY streamlit importer     │
│   @st.cache_data get_data()   wraps analytics.load_data │
│   page config, title, KPI row, trend, breakdowns        │
└─────────────────────────────────────────────────────────┘
```

### Why Streamlit stays out of the lower modules

`analytics.py` and `charts.py` import no Streamlit. Three consequences:

1. **Testable.** pytest imports `analytics` directly with no Streamlit runtime, script context, or
   session state.
2. **Diagnosable.** A wrong number is in `analytics.py`; a wrong-looking chart is in `charts.py`; a
   wrong page layout is in `app.py`. The boundary tells you where to look.
3. **Caching stays a presentation concern.** `load_data` is a pure function. `app.py` wraps it in a
   thin `@st.cache_data` function, which is the pattern Streamlit expects and satisfies the TASK-2
   criterion "data loading is in a reusable, cached function" without coupling the math to the
   framework.

### File layout

```
app.py
analytics.py
charts.py
requirements.txt
.streamlit/config.toml
tests/
  test_analytics.py
data/
  sales-data.csv          (already present)
venv/                     (gitignored)
```

---

## 4. Data Contract

Verified against the actual `data/sales-data.csv` during design:

| Property | Observed value |
|----------|----------------|
| Rows | 482 |
| Distinct `order_id` | 482 (equal to row count) |
| Date range | 2024-01-03 to 2024-12-31 |
| `sum(total_amount)` | 116500.21 |
| `quantity * unit_price == total_amount` | true for all 482 rows |
| Blank fields | none |
| Categories | Accessories, Audio, Electronics, Smart Home, Wearables |
| Regions | East, North, South, West |

Required columns: `date`, `order_id`, `product`, `category`, `region`, `quantity`, `unit_price`,
`total_amount`.

**Total Sales** is `df["total_amount"].sum()`. **Total Orders** is `len(df)`; because distinct
`order_id` equals row count, no distinct-count logic is needed, and a test asserts this invariant so
the assumption is not silently violated by a future data file.

---

## 5. Component Detail

### 5.1 `analytics.py`

`load_data(path)` validates in order and raises `DataError` with a message naming the specific
problem:

1. File exists, else `"Sales data file not found: <path>"`
2. Parses as CSV, else a message naming the parse failure
3. All 8 required columns present, else `"missing required column(s): region"`
4. `date` parses to datetime and `quantity`, `unit_price`, `total_amount` coerce to numeric, else a
   message naming the column and the first offending row

On success it returns a DataFrame with `date` as datetime64 and the three numeric columns as numeric
dtypes.

`DataError` is a custom exception defined in this module. It is the seam that keeps fail-fast
behavior testable: pytest asserts `pytest.raises(DataError)` with no Streamlit present, while
`app.py` catches it and renders the message.

Aggregations:

- `sales_by_week(df)` groups on `df["date"].dt.to_period("W").dt.start_time`, sums `total_amount`,
  returns rows ordered by week ascending.
- `sales_by_category(df)` / `sales_by_region(df)` group and sum, returning rows sorted by
  `total_amount` descending (FR-3, FR-4).

Formatting helpers live here rather than in `app.py` so that FR-1's currency and separator rules are
covered by pytest instead of checked by eye.

### 5.2 `charts.py`

One `PALETTE` constant is used by all three figures so the dashboard reads as one system. Each
builder takes an already-aggregated DataFrame and returns a Plotly figure with axis titles, a hover
template showing the exact value, softened gridlines, and legends suppressed where the axis already
labels the data.

- `trend_chart` — line chart, week-start on X, sales on Y, hover reads "Week of Mar 4 — $3,214"
- `category_chart`, `region_chart` — horizontal bars, highest at top. Horizontal because names like
  "Smart Home" and "Accessories" read cleanly on a Y-axis without rotation, and it matches the PRD's
  mockup.

### 5.3 `app.py`

```
st.set_page_config(layout="wide", page_title="ShopSmart Sales Dashboard")

  ShopSmart Sales Dashboard
  ──────────────────────────────────────────────────
  [ Total Sales  $116,500 ]  [ Total Orders  482 ]      st.columns(2) + st.metric
  ──────────────────────────────────────────────────
  Sales Trend Over Time                                 full width, weekly line
  ──────────────────────────────────────────────────
  Sales by Category        │  Sales by Region           st.columns(2)
  (horizontal bars, desc)  │  (horizontal bars, desc)
```

Error path: `get_data()` is called inside a `try`. On `DataError`, `app.py` renders `st.error` with
the message and calls `st.stop()`, so no partial dashboard with wrong numbers is ever shown (D4).

### 5.4 `.streamlit/config.toml`

Theme block setting primary color, background, and font, plus wide layout. No custom CSS (D6).

---

## 6. Testing

`tests/test_analytics.py`, run with `pytest`.

**Fixture tests** — a 6-row `sample_df()` whose totals are verifiable by hand:

- `total_sales` sums `total_amount`
- `total_orders` counts rows
- `sales_by_category` and `sales_by_region` return descending order
- ties in sort order do not raise
- two dates within the same week collapse into one weekly row
- an empty DataFrame returns empty results rather than raising

**Real-CSV tests** — against `data/sales-data.csv`:

- `total_sales` rounds to 116500.21
- `total_orders` is 482, and equals the distinct `order_id` count
- 5 categories and 4 regions are present
- top category is Electronics

**Validation tests** — temp CSVs written to `tmp_path`:

- missing required column raises `DataError` naming the column
- unparseable date raises `DataError`
- missing file raises `DataError`

**Chart smoke tests** — cheap structural assertions (a figure is returned, with the expected number
of traces) so a typo in `charts.py` fails in pytest rather than in the browser. Visual quality is
verified by running the app, not asserted in tests.

---

## 7. Environment

Plain virtual environment in `venv/`, dependencies in `requirements.txt`: `streamlit`, `pandas`,
`plotly`, `pytest`, pinned to minor versions so that Streamlit Community Cloud resolves the same set
that runs locally.

---

## 8. Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Python 3.14.7 is the only interpreter on this machine** (no 3.11/3.12/3.13). Some pinned wheels may not publish for 3.14 yet. | High — blocks all work | The plan's first step creates the venv and installs dependencies **before** any code is written, so this surfaces immediately rather than mid-build. |
| **Streamlit Community Cloud may not offer Python 3.14** in its interpreter list. | Medium — blocks deploy only | Nothing in this design uses 3.14-only syntax, so selecting 3.13 on Cloud is a valid fallback. Called out explicitly in the deployment handoff step rather than discovered at deploy time. |
| Data quality issues (PRD risk) | High | D4 fail-fast validation, plus validation tests. |
| Scope creep (PRD risk) | High | Phase 2 features are listed as out of scope in section 1 and are not stubbed. |
| Streamlit version churn breaking styling | Low | D6 avoids CSS bound to internal class names. |

---

## 9. Milestone Mapping and Handoff

The implementation plan uses its own sequential numbering (**Step 1, Step 2, ...**) and labels each
step with the milestone it serves, for example `Step 4 (TASK-3)`. The two schemes are kept separate
so they cannot be confused. All eight milestones in `TASKS.md` are covered.

| Milestone | Covered by |
|-----------|------------|
| TASK-1 Environment setup | venv, requirements.txt, project skeleton |
| TASK-2 Data loading and structure | `analytics.load_data`, cached `get_data`, page shell |
| TASK-3 KPI cards | `total_sales`, `total_orders`, formatting helpers, metric row |
| TASK-4 Sales trend chart | `sales_by_week`, `charts.trend_chart` |
| TASK-5 Category and region breakdowns | `sales_by_category`, `sales_by_region`, bar charts |
| TASK-6 Data validation | `DataError`, validation chain, error path in `app.py` |
| TASK-7 Testing and refinement | full pytest run, theme config, browser check |
| TASK-8 Deployment | **user-executed** (see below) |

**Deployment handoff.** The plan stops at a merge-ready state on `feature/sales-dashboard`. TASK-8 is
marked as the user's to execute: the user merges to `main` and deploys to Streamlit Community Cloud
themselves. The plan does not push, does not deploy, and does not modify `main`.
