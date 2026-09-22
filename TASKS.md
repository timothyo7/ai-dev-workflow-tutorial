# TASKS

This file tracks all work for the ShopSmart sales dashboard. Milestones move from **To Do** → **In Progress** → **Done** as they are picked up and completed. Source of requirements: `prd/ecommerce-analytics.md`.

## Definition of Done

Before any milestone moves to Done, all of the following must be true:

- All acceptance criteria for the milestone are met
- The app runs locally with `streamlit run app.py` with no errors or warnings
- The work is committed with the milestone ID (e.g. `TASK-3`) in the commit message

## To Do

### TASK-4 — Sales trend chart (FR-2)
Add a Plotly line chart of sales over time.

- [ ] Line chart plots time on the X-axis and sales amount on the Y-axis
- [ ] Granularity is daily or monthly and axes are clearly labeled
- [ ] Hovering shows a tooltip with the exact value

**Commit:**

### TASK-5 — Category and region breakdowns (FR-3, FR-4)
Add side-by-side bar charts for sales by category and by region.

- [ ] Category bar chart shows all 5 categories, sorted highest to lowest
- [ ] Region bar chart shows all 4 regions, sorted highest to lowest
- [ ] Both charts sit in a two-column layout with interactive tooltips

**Commit:**

### TASK-7 — Testing and refinement (NFR-2, NFR-3)
Polish appearance, verify performance, and clean up the code.

- [ ] Dashboard loads in under 5 seconds with all charts labeled and presentation-ready
- [ ] Code is modular and commented per standard Python practice
- [ ] Verified in at least two modern browsers with no console errors

**Commit:**

### TASK-8 — Deployment to Streamlit Community Cloud (NFR-5)
Deploy the dashboard and share a public URL for stakeholder review.

- [ ] App is deployed to Streamlit Community Cloud from this repo
- [ ] Public URL loads the dashboard with all KPIs and charts working
- [ ] The URL is recorded in `README.md`

**Commit:**

## In Progress

### TASK-6 — Data validation and error handling (FR-5, Risk: data quality)
Validate the CSV structure before loading and fail with a clear message instead of a stack trace.

- [x] Missing file or missing required columns produces a readable in-app message
- [x] Computed totals match the expected values from the CSV
- [ ] No Streamlit or Pandas warnings appear in the terminal

**Commit:** 2b69002

## Done

### TASK-3 — KPI cards (FR-1)
Display Total Sales and Total Orders prominently at the top of the dashboard.

- [x] Total Sales shown as currency with separators (~$116,500)
- [x] Total Orders shown as a count with separators (482)
- [x] Both KPIs appear side by side above the charts

**Commit:** 98b0125

### TASK-2 — Data loading and basic structure
Load `data/sales-data.csv` with Pandas and lay out the dashboard shell (title, sections).

- [x] CSV loads with correct types (date parsed as date, numeric columns as numbers)
- [x] Data loading is in a reusable, cached function
- [x] Page title "ShopSmart Sales Dashboard" and section placeholders render

**Commit:** d51d705

### TASK-1 — Environment setup and project initialization
Set up the Python 3.11+ project, dependencies (Streamlit, Pandas, Plotly), and repo structure.

- [x] `requirements.txt` lists streamlit, pandas, and plotly
- [x] `streamlit run app.py` launches a placeholder app without errors
- [x] Project structure includes `app.py` and `data/` directory

**Commit:** 4d5b752
