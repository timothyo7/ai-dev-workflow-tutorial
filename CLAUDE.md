# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A student working repo for a tutorial that builds a Streamlit sales dashboard from a PRD.
The tutorial docs (`README.md`, `workshop-build-deploy.md`, `codex-companion.md`,
`pre-work-setup.md`, `capstone-tools.md`) are reference material — read them, don't edit them
unless asked. The work happens in the dashboard app and its supporting documents.

## Environment: the venv lives outside the repo

`venv/` in this repo is a **symlink** to `~/.venvs/shopsmart-dashboard`, not a real directory:

```
venv -> /Users/tjoii/.venvs/shopsmart-dashboard
```

This is historical. The repo used to sit at a path containing a `:`, and Python's `venv` module
refuses to build an environment in such a path. The directory has since been renamed and a plain
`python3 -m venv venv` now works here — so a fresh clone needs no workaround. The symlink is kept
because it already works; recreating the venv in-repo is optional cleanup, not a fix.

What still matters:

- Run Python through the venv: `venv/bin/pytest`, `venv/bin/streamlit`, `venv/bin/python`, or
  `source venv/bin/activate` first. A bare `pytest` uses the system interpreter, which has no
  pandas — and the resulting collection error looks like a bug in this project's code.
- The path contains **spaces**, so quote it in shell commands.
- `.gitignore` carries both `venv/` and `/venv`. The first matches directories only, and `venv`
  here is a symlink, so the second entry is what actually ignores it. Don't remove the apparent
  duplicate while the symlink exists.

## Commands

```bash
source venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
streamlit run app.py     # the dashboard
pytest                   # 35 tests; run from the repo root
```

There is no linter or formatter configured in this project — no ruff, black, flake8, or
pyproject.toml. Don't run or reference lint commands that don't exist.

## Architecture: Streamlit is confined to app.py

`analytics.py` and `charts.py` import **no Streamlit at all**, and this is load-bearing rather
than incidental:

- pytest imports them directly with no Streamlit runtime or script context
- a wrong number is in `analytics.py`; a wrong-looking chart is in `charts.py`; a wrong page
  layout is in `app.py`

Follow from this:

- Never add `import streamlit` to `analytics.py` or `charts.py`.
- Caching belongs in `app.py` — `get_data()` wraps the pure `analytics.load_data()` with
  `@st.cache_data`. Do not decorate functions in `analytics.py`.
- `charts.py` takes already-aggregated DataFrames and does no calculation.
- `load_data()` validates strictly and raises `DataError` naming the specific problem; `app.py`
  catches it and calls `st.error` + `st.stop()`. A bad CSV renders nothing rather than a
  half-dashboard with a wrong total.
- Styling is the `[theme]` block in `.streamlit/config.toml` only. No custom CSS — CSS targeting
  Streamlit's internal class names breaks silently across versions.

## Dependencies are split deliberately

`requirements.txt` holds only runtime deps (pandas, plotly, streamlit) because Streamlit
Community Cloud installs exactly that file. Test-only deps go in `requirements-dev.txt`.
Don't merge them.

Pinned: Python 3.14.7, pandas 3.0.6, plotly 7.1.0, streamlit 1.64.0, pytest 9.1.1. These are
newer than much model training data — if a pinned library seems to behave unexpectedly, verify
against the installed version rather than assuming an older API.

## Traceability: TASKS.md is the record

`TASKS.md` is the durable board (To Do / In Progress / Done), not a summary of it. Claude's own
session notes are not the record — the file is.

- Every commit subject leads with its milestone ID: `TASK-4: add weekly sales trend chart`.
  Several IDs are fine when a change closes more than one: `TASK-6 TASK-7: ...`.
- Commit messages are subject, **blank line**, then any trailer. Without the blank line git folds
  the trailer into the subject.
- A milestone moves to Done only when every one of its acceptance criteria is genuinely met, per
  the Definition of Done at the top of `TASKS.md`. If a criterion can't be verified — for example
  a cross-browser check, which needs a human — leave it unticked and leave the milestone in
  In Progress. Don't tick what you can't verify.
- Record the commit SHA on the milestone's `Commit:` line when it's done.

## Workflow for nontrivial changes

This repo exists to practice a specific pipeline, and work here should follow it:

**PRD → TASKS.md milestone → design spec → implementation plan → TDD → commit → review → merge → deploy**

- Requirements come from `@prd/ecommerce-analytics.md`.
- Use the Superpowers `brainstorming` skill to produce a design spec, then `writing-plans` for the
  implementation plan, before writing code.
- Specs and plans are committed to `docs/superpowers/specs/` and `docs/superpowers/plans/`. This
  directory is **tracked deliberately** — don't confuse it with the `dev/` entry directly above it
  in `.gitignore`, which is separate, local-only instructor notes.
- Implement test-first: write the failing test, run it and confirm it fails for the expected
  reason, then implement.
- Work on a feature branch, not `main`.

## Deployment

Streamlit Community Cloud, from `main`, main file `app.py`. `.streamlit/config.toml` and
`data/sales-data.csv` are tracked so they ship with the app. `app.py` builds `DATA_PATH` from
`Path(__file__).parent`, so nothing depends on the working directory Cloud chooses — keep it that
way. Cloud may not offer Python 3.14; nothing here uses 3.14-only syntax, so 3.13 is fine.
