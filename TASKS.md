# TASKS

This file tracks all work for the ShopSmart sales dashboard. Milestones move from **To Do** → **In Progress** → **Done** as they are picked up and completed. Source of requirements: `prd/ecommerce-analytics.md`.

## Definition of Done

Before any milestone moves to Done, all of the following must be true:

- All acceptance criteria for the milestone are met
- The app runs locally with `streamlit run app.py` with no errors or warnings
- The work is committed with the milestone ID (e.g. `TASK-3`) in the commit message

## To Do

## In Progress

## Done

### TASK-9 — Post-merge review fixes (FR-3, FR-4, FR-5)
Fix the two defects found reviewing the merged `feature/sales-dashboard` branch.

- [x] A blank `category` or `region` fails validation instead of silently dropping the row
- [x] The breakdown charts reconcile with the Total Sales KPI
- [x] Validation errors identify the offending row correctly on files with blank lines
- [x] 40 tests pass; the app runs locally with no errors or warnings

**Commit:** d27500a
**Notes:** both defects were invisible rather than loud -- `groupby` drops null keys by
default, and the old `line = row + 2` arithmetic produced a plausible but wrong number.
Errors now name the row by `order_id` rather than by file line, because row position and
file line drift apart the moment pandas skips a blank line. One limitation worth recording:
pandas turns its default null sentinels (`N/A`, `NA`, `null`) into NaN during parsing, so
those values are reported as "an empty value" -- the original text is gone before this
module sees it. Browser render not re-verified; the local run returned HTTP 200 with a
clean log, which is not the same as looking at the page.

### TASK-7 — Testing and refinement (NFR-2, NFR-3)
Polish appearance, verify performance, and clean up the code.

- [x] Dashboard loads in under 5 seconds with all charts labeled and presentation-ready
- [x] Code is modular and commented per standard Python practice
- [x] Verified in at least two modern browsers with no console errors — checked on two
      machines in two different browsers, including a private window

**Commit:** 60fb471
**Notes:** filed as Done while one acceptance criterion was still unticked, which breaks the
Definition of Done at the top of this file; moved back to In Progress until the browser check
was actually made. The cross-browser criterion was reassigned to me — an agent cannot see a
browser render a page, so it should not tick that box.

### TASK-8 — Deployment to Streamlit Community Cloud (NFR-5)
Deploy the dashboard and share a public URL for stakeholder review.

**Live dashboard:** https://sales-dashboard-timothyohara.streamlit.app

- [x] App is deployed to Streamlit Community Cloud from this repo
- [x] Public URL loads the dashboard with all KPIs and charts working — verified in a private
      browser window on a second machine
- [x] The URL is recorded in `README.md`

**Commit:** 69aab73, 3eb1805
**Notes:** the board claimed "daily or monthly" granularity while the code buckets weekly —
a traceability mismatch none of the eight per-milestone reviews caught, because each only saw
its own step; the whole-branch review found it. Claude also reported the deployed app as
private based on a `curl` redirect to an auth URL; that redirect is how Streamlit Cloud mints a
session, and a real browser on a second machine showed it was public all along.

### TASK-6 — Data validation and error handling (FR-5, Risk: data quality)
Validate the CSV structure before loading and fail with a clear message instead of a stack trace.

- [x] Missing file or missing required columns produces a readable in-app message
- [x] Computed totals match the expected values from the CSV
- [x] No Streamlit or Pandas warnings appear in the terminal

**Commit:** 2b69002, 60fb471
**Notes:** clean. The one judgement call: an empty or header-only CSV returns an empty frame
and renders $0 rather than raising, which the spec asks for but sits against this milestone's
own fail-fast rationale. Left as specified, flagged as a decision rather than changed quietly.

### TASK-5 — Category and region breakdowns (FR-3, FR-4)
Add side-by-side bar charts for sales by category and by region.

- [x] Category bar chart shows all 5 categories, sorted highest to lowest
- [x] Region bar chart shows all 4 regions, sorted highest to lowest
- [x] Both charts sit in a two-column layout with interactive tooltips

**Commit:** d0f0eda
**Notes:** clean. `categoryorder="total ascending"` looks inverted but is correct — horizontal
bars render bottom-up, so ascending puts the largest at top; a comment now says so, because it
is the kind of line a future reader would "fix" into a bug.

### TASK-4 — Sales trend chart (FR-2)
Add a Plotly line chart of sales over time.

- [x] Line chart plots time on the X-axis and sales amount on the Y-axis
- [x] Granularity is weekly (see spec D1 — daily is dominated by single-order spikes) and axes are clearly labeled
- [x] Hovering shows a tooltip with the exact value

**Commit:** 07569e9
**Notes:** `use_container_width` is deprecated on Streamlit 1.64 and emitted a warning. Left
in place deliberately rather than patched here, so all three chart call sites could be swept to
`width="stretch"` in one pass once the actual warning text was known.

### TASK-3 — KPI cards (FR-1)
Display Total Sales and Total Orders prominently at the top of the dashboard.

- [x] Total Sales shown as currency with separators (~$116,500)
- [x] Total Orders shown as a count with separators (482)
- [x] Both KPIs appear side by side above the charts

**Commit:** 98b0125
**Notes:** clean.

### TASK-2 — Data loading and basic structure
Load `data/sales-data.csv` with Pandas and lay out the dashboard shell (title, sections).

- [x] CSV loads with correct types (date parsed as date, numeric columns as numbers)
- [x] Data loading is in a reusable, cached function
- [x] Page title "ShopSmart Sales Dashboard" and section placeholders render

**Commit:** d51d705
**Notes:** commit message put the `Co-Authored-By` trailer on line 2 with no blank line, so git
folded it into the subject and `git log --oneline` printed it inline; amended. Caught because
the board records SHAs and the history is the deliverable.

### TASK-1 — Environment setup and project initialization
Set up the Python 3.11+ project, dependencies (Streamlit, Pandas, Plotly), and repo structure.

- [x] `requirements.txt` lists streamlit, pandas, and plotly
- [x] `streamlit run app.py` launches a placeholder app without errors
- [x] Project structure includes `app.py` and `data/` directory

**Commit:** 4d5b752
**Notes:** `python3 -m venv venv` refused to run — the repo path contained a `:`, which the
venv module rejects outright. First workaround put the venv in `/tmp` (not durable) and left
the symlink untracked, because `.gitignore`'s `venv/` matches directories only; both fixed.
The directory was later renamed to drop the colon, so the workaround is now historical.
