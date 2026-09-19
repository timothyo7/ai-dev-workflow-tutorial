# Part 2: Build & Deploy

**From requirements to a live dashboard using skill-driven development.**

**Format:** Self-paced, about 3 hours

**Written against:** Claude Code 2.1 and Superpowers 6.3.0, September 2026. Both update themselves, so a menu or a skill's wording may differ a little from what's quoted here. The shape of each step stays the same.

---

## Table of contents

- [How to work through this guide](#how-to-work-through-this-guide)
- [Section 1: Set up your task board from the PRD (~15 min)](#section-1-set-up-your-task-board-from-the-prd-15-min)
- [Section 2: Brainstorm and plan (~30 min)](#section-2-brainstorm-and-plan-30-min)
  - [2.1 Create the feature branch](#21-create-the-feature-branch)
  - [2.2 Brainstorm and plan with one prompt](#22-brainstorm-and-plan-with-one-prompt)
- [Section 3: Two artifacts, two altitudes (~5 min)](#section-3-two-artifacts-two-altitudes-5-min)
- [Section 4: Build the dashboard (~45 min)](#section-4-build-the-dashboard-45-min)
  - [4.1 Implement the first milestone](#41-implement-the-first-milestone)
  - [4.2 Commit, push, and update TASKS.md](#42-commit-push-and-update-tasksmd)
  - [4.3 Complete remaining milestones](#43-complete-remaining-milestones)
  - [4.4 Capture project memory with /init](#44-capture-project-memory-with-init)
  - [4.5 Review, then merge to main](#45-review-then-merge-to-main)
- [Section 5: Deploy (~15 min)](#section-5-deploy-15-min)
- [Section 6: Final verification checklist](#section-6-final-verification-checklist)
- [Section 7: Turn in your work](#section-7-turn-in-your-work)
- [Troubleshooting](#troubleshooting)
- [Other Superpowers skills you'll meet later](#other-superpowers-skills-youll-meet-later)
- [Glossary](#glossary)

---

## How to work through this guide

This guide is self-paced. Work through it top to bottom; each section builds on the one before it, so don't skip ahead. Most people finish in about three hours, but there's no clock: do it in one sitting or split it across a few sessions, whatever fits your schedule. (The per-section time labels add up to well under three hours because they only count the hands-on steps; the rest is reading, answering brainstorming's questions, and watching Claude build.) You'll save your progress with Git as you go (Section 4), so you can stop and pick up later without losing anything.

> **Using Codex instead of Claude Code?** Every prompt in this guide works the same way in Codex, because the Superpowers skills run on both. The places that differ (starting a session, permission modes, the output style, `/init`, the code review command) are marked **Codex:** in the [Codex companion](codex-companion.md). Keep it open in a second tab.

> **Small things Claude Code shows that this guide doesn't cover.** A pasted prompt collapses to "[Pasted text #1 +5 lines]" in the input box; it's all there. A one-line "How is Claude doing this session?" rating appears now and then; press 0 or just keep typing. Tips about /ultrareview, approving from your phone, remote control, or a fullscreen renderer are offers, not steps, so ignore them or say no. None of these change what you do next.

> **Didn't finish the setup yet?** Work through the [setup guide](pre-work-setup.md) first; most people finish it in under an hour. Then come back and complete the build here. Ask in the Teams General channel, or send me a direct message on Teams, if you get stuck.

---

## What you'll accomplish

By the end of this guide, you'll have taken a product requirements document through a full development workflow and produced a live analytics dashboard. Specifically, you'll have:

- Set up an in-repo `TASKS.md` board of milestones drawn from the PRD, with a shared Definition of Done
- Generated Superpowers artifacts: a design document and an implementation plan
- Moved each milestone from To Do to Done as you build
- Built a working Streamlit dashboard with AI-assisted coding
- Generated a `CLAUDE.md` with `/init` so the project carries its own context
- Committed and pushed code to GitHub with traceability from each milestone to its commits
- Deployed a live dashboard accessible by anyone with the URL

---

## Prerequisites check

Before starting, verify your Part 1 setup is complete. Open your cloned `ai-dev-workflow-tutorial` folder in VS Code first (File --> Open Folder); the terminal then opens at the project root, which is where these commands expect to run. Run each command in VS Code's terminal:

```bash
git --version
# Expected: git version 2.x.x

python3 --version       # macOS
python --version         # Windows
# Expected: Python 3.11.x or higher

ls data/sales-data.csv
# Windows cmd: dir data\sales-data.csv
# Expected: data/sales-data.csv (no error)

claude --version
# Expected: version number displayed
```

If any command fails, return to the [setup guide](pre-work-setup.md) and resolve the issue before proceeding. Make sure everything's working before you continue.

> **Heads up:** Websites and software update their interfaces regularly. A button label, sign-up flow, or menu option described here may look slightly different by the time you go through it. That's normal. Focus on the goal of each step rather than the exact clicks: once you know what a step is trying to accomplish, you can usually find the equivalent option even when the UI has moved. Read the screen, work it out, and keep going. Figuring things out on your own like this is itself a professional skill.

---

## The professional workflow

This is the workflow used at technology companies worldwide. You'll experience the entire cycle, from specification to deployment. This tutorial calls the approach *skill-driven development*. A *skill* here is a small, reusable piece of expertise Claude pulls in when it fits the task; instead of jumping straight to code, you let a chain of these skills run the work in order (brainstorm the design, plan the steps, then build), so the project has a clear shape before Claude writes anything.

```
┌─────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌────────┐
│   PRD   │ -> │   TASKS.md   │ -> │ brainstorming│ -> │writing-plans │ -> │  Code  │
│(written)│    │ (milestones) │    │ (design doc) │    │ (impl plan)  │    │(Claude)│
└─────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └────────┘
                                                                              │
┌─────────┐    ┌───────────┐    ┌─────────┐    ┌───────────────────────────────┐
│  Live!  │ <- │  Deploy   │ <- │  Push   │ <- │ executing-plans (TDD + commit)│
│(public) │    │(Streamlit)│    │(GitHub) │    │ on a feature branch           │
└─────────┘    └───────────┘    └─────────┘    └───────────────────────────────┘
```

Each box in this diagram is a distinct stage you'll complete. The left-to-right flow on the top row moves from planning to execution. The right-to-left flow on the bottom row moves from saving your work to making it publicly available. Together, they form a closed loop: requirements become running software that stakeholders can access.

> **Why skill-driven development?** You could ask Claude "build me a dashboard" directly. But without a clear plan, Claude makes assumptions, and AI can build the wrong thing very fast. Superpowers' skills give the work structure: brainstorming explores what to build, writing-plans turns the design into a bite-sized plan, and executing-plans implements one task at a time. Letting the skills run their process is what makes AI-assisted coding predictable instead of chaotic. The same habit will help keep a bigger capstone project from drifting.

---

## Section 1: Set up your task board from the PRD (~15 min)

### Tracking work in a file

Professional teams track every piece of work so they always know what's done, what's in progress, and what's next. Many use a web app like Jira for this. In this tutorial, you'll track work in a single Markdown file that lives in your repository: `TASKS.md`.

Here is the difference:

```
Web-app tracker (e.g. Jira)          File-based tracker (TASKS.md)
┌──────────────┐                     ┌──────────────┐
│  Claude Code │                     │  Claude Code │
│  (terminal)  │                     │  (terminal)  │
└──────┬───────┘                     └──────┬───────┘
       │ needs a connector                 │ just opens a file
       │ + account + login                 │
       v                                    v
┌──────────────┐                     ┌──────────────┐
│  Jira (cloud)│                     │  TASKS.md     │
│  separate    │                     │  in your repo │
│  website     │                     │  next to code │
└──────────────┘                     └──────────────┘
```

> **Why track work in a file?** A Markdown file has real advantages for a project like this one:
> - **No extra account or connection.** Claude Code can already read and write files in your project, so it updates your task board directly, with no web app to switch to and no login to keep alive.
> - **Versioned with your code.** `TASKS.md` is committed to Git alongside `app.py`. At any point in history, the task board and the code are in sync. Run `git log -- TASKS.md` and you can see exactly how the work evolved: the same audit trail a tracker like Jira gives you, built into your repo.
> - **Diffable and reviewable.** Changes to tasks show up in your commits and diffs like any other file.
> - **It works offline and travels with the project.** The same file works in Claude Code, VS Code, or any editor.
>
> This is a real, current industry pattern, not a training-wheels version. Teams building with AI coding agents increasingly keep their task lists in the repo so the agent can read and update them directly. (The open-source tool [Backlog.md](https://github.com/MrLesk/Backlog.md) formalizes the same idea at larger scale.)

### Your board is the record, not Claude's notes

Claude Code keeps notes of its own. While it works you may see progress checklists in its output. At the end of a session it may say something like "Saved 2 memories," which means it wrote down something it learned about your project in a private file (more on that in Section 4.4). Neither of those is your record. They're Claude's working notes, and nobody grades them.

`TASKS.md` is different. It's the **durable** record you commit to Git. It survives new sessions, grading, and your own memory a month from now. When this guide says "update your task board," it always means the file.

### Steps

1. **Start Claude Code** from your project directory in VS Code's terminal. To open one, go to **Terminal** --> **New Terminal** in the menu bar (or press `` Ctrl+` ``). Then run:

   ```bash
   claude
   ```

   The first time you start Claude Code in this folder, it asks whether you trust the folder. The highlighted answer is **No, exit**, so press the down arrow to **Yes, I trust this folder** and press Enter. Superpowers loads automatically for the session (you installed and verified it in Part 1). If you're not sure it's active, ask Claude `Is the Superpowers plugin installed?`

2. **Set the output style to Explanatory.** Inside Claude Code, open the settings menu:

   ```
   /config
   ```

   The settings list is long, so type **output** in its search box to narrow it, then press **Enter**. Use the **arrow keys** to highlight **Output style** and press **Enter** again. Highlight **Explanatory**, press **Enter** to confirm, and press **Esc** to close the config menu. (Depending on your terminal, you may also be able to click an option with your mouse, but the arrow keys always work.) By default, Claude Code keeps its responses short; the Explanatory style tells Claude to explain what it's doing and why as it works, which helps you learn from it instead of just receiving code. The choice saves to your project's `.claude/settings.local.json` and persists, so you only set it once.

   A style loads when a conversation starts, so it isn't active in the one you're in yet. Restart the conversation:

   ```
   /clear
   ```

   > **Prefer editing the file?** You can set the same thing directly by adding `"outputStyle": "Explanatory"` to `.claude/settings.local.json`, then run `/clear`.

   > **Want to write some of the code yourself?** The **Learning** style goes a step further than Explanatory: Claude leaves small, clearly marked pieces of the code for you to fill in. If you already know some Python and want the practice, pick it instead. You can switch back to Explanatory at any time from the same menu.

3. **Read the PRD first.** Your task board should reflect what the project needs to deliver, and that's spelled out in the product requirements document.

   > **What is a PRD?** A PRD (Product Requirements Document) is a written description of what you're building and why. It defines the problem, the users, the features, and what success looks like. It doesn't come out of thin air: someone (usually a product manager or business analyst) interviews the stakeholders, the people who will use the product or are paying for it, to learn what they actually need, then writes those needs down as requirements. In professional settings, the PRD is agreed on before any code is written. (For this tutorial, we've written the PRD for you so you can focus on the build; in your capstone, you'll gather requirements from your own stakeholders.)

   Open the [PRD](prd/ecommerce-analytics.md) and skim it (in your browser, or open `prd/ecommerce-analytics.md` in VS Code). Look at two sections in particular: **Acceptance Criteria** and **Timeline and Milestones**. The PRD already sketches the deliverables your board will track; you're not inventing them from scratch.

4. **Create your task board from the PRD.** Ask Claude Code to draft it:

   ```
   Read @prd/ecommerce-analytics.md. Create a TASKS.md file in the project root with:
   - a short note at the top saying this file tracks all work for the dashboard
   - a "Definition of Done" section: a short list, without checkboxes, of what must be true before any milestone moves to Done: acceptance criteria met, app runs locally with `streamlit run app.py`, changes committed with the milestone ID in the message
   - a "To Do" section with 4-8 milestones based on the PRD's deliverables and its Milestones table, numbered TASK-1, TASK-2, and so on, each with a one-line description, 1-3 acceptance criteria as checkboxes, and a "Commit:" line left blank for me to fill in when it's done
   - empty "In Progress" and "Done" sections
   ```

   > **The `@` symbol: pointing Claude at a file.** This is the first time you use it. `@prd/ecommerce-analytics.md` tells Claude Code to pull that exact file into the conversation, so it works from the real contents instead of guessing or making you copy and paste them. You can point at a whole folder the same way (like `@docs/superpowers/plans/`). When you type `@`, Claude Code shows a list of files and folders and autocompletes the path as you go, so you rarely type the whole thing. Pointing the AI at the right file is a small habit with a big payoff. You get better output, because the more precisely you set the context, the more on-target the result. And you get faster, cheaper output: because Claude reads just the file you named, it doesn't burn time and tokens (the chunks of text a model processes) searching your project for the right context, which means quicker replies and more headroom before you hit your plan's usage limits. You'll use `@` throughout the rest of this guide.

   Claude reads the PRD and drafts the board. Open `TASKS.md` in VS Code and read it. It should look roughly like this:

   ```markdown
   # Sales Dashboard: Tasks

   This file tracks all work for the e-commerce sales dashboard.
   Each milestone moves through To Do -> In Progress -> Done.

   ## Definition of Done (must hold before any milestone moves to Done)
   - Acceptance criteria met
   - App runs locally with `streamlit run app.py`
   - Changes committed with the milestone ID in the message

   ## To Do
   - [ ] **TASK-1: Project setup and data loading**
     - [ ] App runs with `streamlit run app.py` and shows a title
     - [ ] Loads `data/sales-data.csv`; handles a missing file cleanly
     - Commit:
   - [ ] **TASK-2: KPI scorecards**
     - [ ] Total Sales and Total Orders shown as formatted metrics
     - Commit:
   - [ ] **TASK-3: Sales trend chart**
     - [ ] Line chart of sales over time renders from the data
     - Commit:
   - [ ] **TASK-4: Category and region breakdowns**
     - [ ] Bar charts for sales by category and by region, sorted by value
     - Commit:
   - [ ] **TASK-5: Test and deploy**
     - [ ] Dashboard runs without errors and is deployed to a public URL
     - Commit:

   ## In Progress

   ## Done
   ```

   Your milestones may differ a little, and that's fine. Read them against the PRD and adjust anything that doesn't match what you want to build. You're aiming for a short list you could read aloud in a status update: the *what*, not the *how*. (Superpowers works out the *how* in the next section.)

   > **What is a Definition of Done?** It's a short standard that applies to *every* milestone, no matter what it is. Each milestone also gets its own **acceptance criteria** (the specific thing that milestone must do). The Definition of Done is the shared bar underneath all of them: "before I call anything done, these things are always true." You don't tick it off; you make sure it holds each time you move a milestone to Done. Professional teams agree on a Definition of Done so "done" means the same thing to everyone. The blank **Commit:** line under each milestone is where you'll record the commit that finished it (Section 4.2).

**Checkpoint:** `TASKS.md` exists in your project root with a Definition of Done and 4-8 milestones (TASK-1, TASK-2, ...) in the To Do section, drafted from the PRD.

---

## Section 2: Brainstorm and plan (~30 min)

### Understanding skill-driven development

The rest of the tutorial flows from what you create here. Every step that follows (coding, committing, deploying) depends on the design and plan you produce in this section.

> **The problem with "just code it":** When you ask an AI to build something without a clear design, you get something that might work but probably isn't what you wanted. The AI fills in gaps with assumptions, and each assumption is a potential mismatch with your intent. With a deliverable like an analytics dashboard, even small mismatches compound: the wrong chart type, unexpected aggregation, a layout that doesn't serve the audience.

Superpowers solves this by chaining three skills:

```
brainstorming -> writing-plans -> executing-plans
(design doc)    (impl plan)      (code, tested, committed)
```

Each skill narrows the space of possible outcomes. By the time executing-plans runs, Claude knows what to build, how to build it, and in what order. The result is more likely to match what you actually wanted.

### 2.1 Create the feature branch

Before you build anything, you'll set up a separate branch to work on. If you're new to Git, here's what that means and why it matters.

> **What is a branch, and why make one?** A **branch** is a separate line of work in your project, like a parallel copy you can change freely without touching the original. Your project already has one branch, called `main`: the official, working version of the code. Instead of building directly on `main`, you'll make a new branch just for this dashboard (a **feature branch**) and do all your work there. That keeps `main` clean and stable, so if something breaks while you build, the trusted version stays safe. When the feature is finished and tested, you merge your branch back into `main` (Section 4.5). This is how professional teams work: build on a branch, then merge.

You could type the Git command yourself, but you don't have to. In Claude Code, just ask:

```
Create a new git branch called feature/sales-dashboard and switch to it.
```

Claude runs the command and confirms you're on the new branch.

The name `feature/sales-dashboard` follows a common convention: a `feature/` prefix plus a short, hyphenated description of what you're building. You'll name your own branches this way in the capstone, so a branch says at a glance what work it holds.

> **This is the whole idea.** You don't memorize Git commands in this tutorial. When you need one, describe what you want and let Claude Code run it. It'll show you the command it used (here, `git checkout -b feature/sales-dashboard`), so you pick up the vocabulary as you go instead of drilling it up front.

**Checkpoint:** Ask Claude "which branch am I on?" It should be `feature/sales-dashboard`.

Now that you're on your feature branch, save the task board you created in Section 1 so it's under version control. In Claude Code:

```
Commit TASKS.md with the message "Add task board from the PRD".
```

From here on, your board lives in Git. It's saved locally for now; you'll push it to GitHub in Section 4, along with your first milestone (that's when the guide covers pushing). As you finish each milestone, you'll commit an update to the board.

> **Optional Pro Tip: keep your bearings on screen.** Instead of asking which branch you're on each time, you can pin a status line to the bottom of Claude Code that shows it all the time. Ask it once:
>
> ```
> /statusline show the current git branch, the folder, the model, the reasoning effort, and the context usage
> ```
>
> Claude writes the setup for you (no scripting needed), and it appears in every session from then on, including your capstone. This is a nice-to-have, not part of the build, so if it doesn't render cleanly on your machine, just skip it.

### 2.2 Brainstorm and plan with one prompt

This is the moment the workflow shifts from "you driving Claude" to "Claude running a process you observe." You already know the *what*: the milestones on your board. Now you give Claude one prompt; the brainstorming skill activates, asks you questions, writes a design doc, and hands off to writing-plans, which produces an implementation plan for the *how*. You'll see each skill load in the output as it activates.

1. **Send the prompt.** In your Claude Code session (still open from Section 1), send the prompt below. It points at the PRD and your milestones, and sets a few ground rules so the plan fits this project:

   ```
   Help me design and plan the e-commerce sales dashboard described in
   @prd/ecommerce-analytics.md. Start by brainstorming the design with me:
   ask me your clarifying questions one at a time, and write a design doc
   for my review before any plan. I'm tracking the milestones in @TASKS.md.
   Structure the plan so its steps cover each one, and label every plan
   task with the milestone it belongs to (TASK-1, TASK-2, and so on).
   Keep the plan's own task numbering separate so the two don't get mixed
   up. Make deployment the final step of the plan, marked as mine to
   execute: I'll deploy it myself from the main branch after we merge, so
   the plan should stop there and hand off to me. Ground rules: work on my
   current feature branch (do not create a git worktree), use a plain
   Python virtual environment in venv/ with a requirements.txt for
   dependencies (no uv or conda), keep the data calculations in their own
   module with pytest tests, and keep the code simple and readable so I
   can follow it.
   ```

   > **What those ground rules mean.** You're setting these constraints on purpose, not parroting them:
   > - **start by brainstorming the design with me.** Superpowers has a brainstorming skill for exactly this, but Sonnet 5 skips it when the PRD looks complete enough to plan from, and goes straight to writing the plan. Asking for the brainstorm in plain words is what gets you the interview in step 2.
   > - **label every plan task with its milestone.** The plan will have its own task numbers. Asking for the milestone ID on each one keeps the two from getting confused, and it's what lets a commit message say `TASK-2` and mean your board.
   > - **deployment is planned, but marked as yours.** Real plans include deployment; what a professional team controls is who executes it. Publishing needs your accounts (GitHub, Streamlit) and a go/no-go call, so the plan carries the step but stops and hands it to you: you'll run it yourself in Section 5, from `main`, after the merge. This is a prompt pattern worth reusing on any AI-planned project: mark the steps that publish work or need your credentials as human-executed.
   > - **do not create a git worktree.** A *worktree* is a separate working copy of your project. Superpowers would normally make one, but you keep things simple by staying on the single feature branch you created (more in the skills table at the end).
   > - **use a plain virtual environment in `venv/` with a `requirements.txt`.** The virtual environment is a private space for this project's Python packages, so they don't clash with anything else on your machine. Claude sets it up while building, and it's explained where you use it in Section 4.1. The `requirements.txt` is the list of packages, and it's the file Streamlit Cloud reads when you deploy in Section 5. Naming both keeps Claude from reaching for a different tool (there are several) and handing you something the deploy step doesn't expect.
   > - **keep the data calculations in their own module with pytest tests.** Left to its defaults, brainstorming recommends one big `app.py` and no automated tests, and the test-first steps in Section 4 need both. Calculations in their own file are also what makes them testable without starting the dashboard.
   > - **keep the code simple and readable,** so you can follow what gets built, which is the whole point.
   >
   > Giving the AI clear constraints like these is itself a skill: you get a plan shaped to *your* project instead of its defaults.

2. **Answer brainstorming's questions.** Claude loads the brainstorming skill (you'll see a `Skill(superpowers:brainstorming)` line with `Successfully loaded skill` under it). The first thing it tells you is how big it thinks the job is. A new dashboard counts as *architectural*, the fullest path, so expect the whole conversation described here. Then it asks clarifying questions, one at a time, on things like the trend chart's granularity, what to do if the data file is missing, and how to organize the files. Each comes as a short menu with a recommended option; pick the one that fits your vision, or type your own preference. After the questions it lays out the design in sections and asks whether it looks right. Some runs take it more slowly, proposing two or three approaches first and checking after each section. A yes moves it along. A change request is welcome at any point, and it's cheaper here than anywhere later.

   > **If it offers to "show you" in a browser:** brainstorming can open a companion page in your browser for mockups and diagrams. Say no, thanks. It spends usage you'll want for the build, and everything in this tutorial happens in the terminal.

3. **Review the design doc (your chance to change it).** Brainstorming writes a design doc to `docs/superpowers/specs/YYYY-MM-DD-sales-dashboard-design.md` and commits it, then pauses and asks you to review it before turning it into a plan (something like *"give the spec a read and let me know if you want any changes; if it looks right, say the word and I'll draft the plan"*). This is the most important checkpoint in the process: the design is about to drive the plan and then the code, so now is the moment to catch anything wrong or missing, while it's cheap to fix. Open the file in VS Code and read it: in the Explorer on the left, expand the `docs` folder, then `superpowers`, then `specs`, and click the design doc to open it. (No sidebar? Press `Cmd+B` on macOS or `Ctrl+B` on Windows to toggle it.) It opens as raw Markdown, so to read it as a formatted document, press `Cmd+Shift+V` (macOS) or `Ctrl+Shift+V` (Windows), or click the **Open Preview to the Side** icon in the editor's top-right corner. If anything is off (a wrong chart type, a missing KPI, an assumption you disagree with), just tell Claude what to change and it will revise the spec. Keep going until the spec captures what you want.

4. **Approve the spec, then review the plan.** When the spec captures what you want, tell Claude to proceed. In Claude Code:

   ```
   The spec looks good. Go ahead and write the implementation plan.
   ```

   Claude hands off to writing-plans (you'll see a `Skill(superpowers:writing-plans)` line with `Successfully loaded skill` under it, just like the brainstorming skill earlier), which produces an implementation plan at `docs/superpowers/plans/YYYY-MM-DD-sales-dashboard.md`. Open it the same way (expand `docs`, then `superpowers`, then `plans`, then preview it) and read it. The plan contains bite-sized tasks; some are flagged for test-driven development (TDD), typically data transformations like KPI calculations and date filtering. Also check the plan's last step: it should be deployment, marked as yours to execute from `main` after the merge, exactly as you asked in the prompt. The design doc captures *what* to build; the plan captures *how* to build it, task by task.

5. **Choose how Claude will execute the plan.** After the plan is written, Claude asks one last question before any code runs: how do you want it to execute the plan? You'll usually see two options:

   - **Subagent-driven**: Claude hands each task to a fresh helper agent (a *subagent*) that works on it separately, reviews the result, and moves to the next task without stopping to ask you. Picture delegating each task to a new contractor who starts with a clean slate: nothing from earlier tasks clutters their head, so mistakes get caught early. The tradeoff is that the work happens offstage. You see the reports, not the process.
   - **Inline execution**: Claude does every task itself, right in your session. Each test, file, and decision scrolls past on your screen as it happens.

   For this tutorial you want **inline execution**: watching the process is the point, and it keeps everything in one conversation. Claude may add that Superpowers works better with subagents. That's true for speed, and it's the mode you'll probably use on a capstone, once you've seen what happens inside. Answer now, but tell Claude to wait before building, since you have a bit of reading to do first:

   ```
   Use inline execution, but wait for my go-ahead before starting the first
   task.
   ```

   Claude loads `executing-plans` as soon as you answer (the `Skill(superpowers:executing-plans)` line appears now), reads the plan, and waits. You'll give that go-ahead in Section 4.1, after a short look at how the plan relates to your task board.

> **Why write this down before any code runs?** The hard part of any project is the thinking: framing the problem, choosing an approach, weighing tradeoffs. That's exactly the part it's tempting to hand to the AI, and exactly the part you learn the most from keeping. Writing the spec and plan first forces your reasoning onto the record, where you and a reviewer can see it, instead of letting it disappear into the tool. The two files you just read are that record.

> **Why TDD on some tasks?** Some plan tasks are flagged for **test-driven development (TDD)**: Claude writes a small test before the code, so the behavior is pinned down before anything is built. It's used on data transformations like KPI calculations and date filtering, and skipped for chart rendering, where Streamlit components are hard to test meaningfully. Whether test-first makes an *agent's* code better is an open question. One careful experiment in August 2026 found no difference in quality and several times the cost. This tutorial keeps it anyway, for you rather than for Claude. A failing test is the one artifact in the build that's short enough to read in full, and it says exactly what "correct" means for that piece. When one appears in Section 4, read it before Claude writes the code, and say in one sentence what it checks. That sentence is what the walk-through will ask you for.

> **Skill handoff cheat sheet (the chain you just experienced):**
>
> ```
> [you type one prompt]
>      |
>      v
> using-superpowers (auto)
>      |
>      v
> brainstorming  -> sizes the job, asks Qs, proposes approaches,
>                   writes design doc, gets your approval
>      |
>      v  (skipped worktree per your prompt)
> writing-plans  -> produces plan with TDD-flagged tasks
> ```
>
> In Section 4 the chain continues: `executing-plans` builds task by task, then `requesting-code-review` and `finishing-a-development-branch` wrap up. Each skill shows up as a `Skill(superpowers:<name>)` line, so if you lose track, scroll up to the most recent one.

Superpowers commits the design doc and the plan as it writes them, so there's usually nothing left to commit here. Check anyway, so you know both documents sit in your history before any code does. In Claude Code:

```
Make sure the design doc and the implementation plan are both committed,
then show me the commit history.
```

**Checkpoint:** You have two new files: a design doc in `docs/superpowers/specs/` and an implementation plan in `docs/superpowers/plans/`. The history Claude shows has the board, the design doc, and the plan each as a commit, and no code yet. That order is the point. The thinking is on the record before the building starts.

---

## Section 3: Two artifacts, two altitudes (~5 min)

You now have two planning documents. Being clear on how they relate matters; this is where students most often get confused.

- **`TASKS.md`** holds your **milestones**: the coarse deliverables you drafted from the PRD in Section 1. This is the *what*, and the board you track status on.
- **The implementation plan** (`docs/superpowers/plans/...`) holds the **detailed steps** Superpowers just produced. This is the *how*, and the checklist Claude builds from.

> **The two artifacts, and why they don't overlap:**
>
> | | `TASKS.md` | Implementation plan |
> |---|---|---|
> | **Lives in** | project root | `docs/superpowers/plans/` |
> | **Granularity** | Coarse (~4-8 milestones) | Fine (every engineering step) |
> | **Comes from** | the PRD, up front (Section 1) | brainstorming + the design doc (Section 2) |
> | **Updated by** | you, with Claude's help | Superpowers (`executing-plans` checks steps off as it builds) |
> | **Answers** | "What's the status of the dashboard?" | "What's the next step to code?" |
> | **Audience** | you, your grader, a stakeholder | Claude (the builder) |
>
> `TASKS.md` is the "what and where-are-we." The plan is the "how." One milestone on your board covers several steps in the plan; they're two zoom levels of the same work, not two copies of it. You track from the board; Claude builds from the plan.

```
TASKS.md (your milestones)              Implementation plan (Claude's steps)
┌────────────────────────────┐          ┌────────────────────────────┐
│ TASK-1 Project + data      │ <──────  │ scaffold app.py             │
│        loading             │ <──────  │ add requirements.txt        │
│                            │ <──────  │ load + validate CSV         │
├────────────────────────────┤          ├────────────────────────────┤
│ TASK-2 KPI scorecards      │ <──────  │ compute_total_sales + test  │
│                            │ <──────  │ render KPI metrics          │
├────────────────────────────┤          ├────────────────────────────┤
│ TASK-3 Sales trend chart   │ <──────  │ build trend chart           │
│ ...                        │          │ ...                         │
└────────────────────────────┘          └────────────────────────────┘
  You set these (from the PRD)            Superpowers wrote these (the how)
```

**Checkpoint:** You can pick any step in the implementation plan and say which milestone on your board it belongs to.

> **Pro Tip:** Notice the zoom levels. The PRD said "display Total Sales." The plan breaks that into steps ("compute total sales with a test," "render a metric component"). Your board zooms back out to one milestone: "KPI scorecards." Same work, three altitudes: requirement, engineering steps, trackable deliverable. Being able to move between them is a real skill.

---

## Section 4: Build the dashboard (~45 min)

### Understanding Streamlit

> **What is Streamlit?** Streamlit is a Python library that transforms Python scripts into interactive web applications. Instead of writing HTML, CSS, and JavaScript (the traditional technologies for building web pages), you write Python and Streamlit handles the web interface automatically. It's especially popular in data science and business analytics because it lets analysts create dashboards quickly using the language they already know.
>
> For example, this Python code:
> ```python
> import streamlit as st
> st.title("Sales Dashboard")
> st.metric("Total Sales", "$116,500")
> ```
> produces a web page with a title and a formatted metric card. No HTML needed.
>
> Streamlit isn't the only option for dashboards (Tableau, Power BI, and Dash are alternatives), but it works well for capstone projects: it uses pure Python, integrates with Pandas and Plotly, and deploys for free. You can use the same data manipulation skills you learned in your coursework.

### Claude Code permission modes

Before you start building, understand how much Claude Code does on its own. A **permission mode** sets which actions Claude takes without asking you first:

| Mode | What Claude does on its own | When to use it |
|------|-----------------------------|----------------|
| **Manual** | Nothing much. It asks before editing a file or running most commands | When you want to see every move, like your first milestone |
| **Accept edits** | Edits files without asking, still asks before most commands | When you trust the edits but want to watch the commands |
| **Plan** | Reads and proposes only. Changes nothing until you approve the plan | When you want to review an approach before anything happens |
| **Auto** | Edits and runs commands on its own. A second, checking model watches each action and blocks the risky ones: destructive Git commands, reaching outside the project, or anything a file it read tries to make it do | When you know what it's doing and want momentum. On a Pro plan, every new session starts here |

Press **Shift+Tab** to cycle between modes. The label at the bottom of the Claude Code window changes with each press.

> **Recommendation: Manual for TASK-1, Auto after that.** For your first milestone, press Shift+Tab until you're in Manual, then build. You'll approve each file write and each command (`pytest`, `git commit`, and so on). That's a lot of Enter-pressing for one milestone, and worth doing once: you see exactly what an agent does to a project, and nothing happens that you didn't say yes to. From TASK-2 on, switch to Auto and let it run. That's how you'll work on a capstone, and by then you'll know what's happening behind the curtain. Anthropic's own numbers back this order. People who approve every action stop reading what they approve, and those sessions ran into serious mistakes about twice as often as Auto sessions did. Seeing it once teaches you something. Clicking through it forty times doesn't.

### 4.1 Implement the first milestone

Milestones are in plan order, so you'll work top-down: TASK-1 first. Within a milestone, Claude works through the plan steps it covers, one at a time.

1. Back in Section 2.2 you told Claude to wait for your go-ahead. This is it. Press **Shift+Tab** until you're in Manual mode (see the modes above), then start the first milestone and move it to In Progress on your board:

   ```
   Let's work on TASK-1. Move it to the In Progress section of TASKS.md, then
   implement the plan steps it covers.
   ```

   `executing-plans`, loaded back in Section 2.2 step 5, reads the plan and works through the steps under this milestone, one at a time. In Manual mode it asks before its first file write, which is how you know the mode took.

   > **What you'll see during a TDD step:** For plan steps flagged as test-driven (typically data-transformation steps like `compute_total_sales`), executing-plans will: (a) write a failing test in a `tests/` file, (b) run pytest (Python's test runner) and show you the failure, (c) implement the function, (d) run pytest again and show you the pass, (e) commit. For non-TDD steps (chart rendering, page layout), it'll skip straight to implementation and commit. A single milestone may contain several such steps. When the failing test appears at (a), read it before (c) happens. In Manual mode, Claude is waiting for you anyway. Say to yourself what it checks: "total sales is the sum of the total_amount column." That's the sentence the walk-through asks for. Then watch the test output: seeing red turn green is one of the more satisfying parts of the build.

   > **What happens during implementation:** Claude reads the task and its acceptance criteria, consults the specification and plan, then writes the code. Watch the output; you'll see Claude creating files, writing functions, and making decisions. Pay attention to which libraries Claude imports, how it structures the code, and how it handles data loading.

   > **How Claude moves through the milestone:** Your prompt scoped the work to TASK-1, so executing-plans works through that milestone's plan steps and then stops and reports: what it built, what the tests showed, and what comes next. Claude may mention that Superpowers runs faster with subagents. For this milestone, stay inline. Watching is the point. If it offers to roll straight into the next milestone's steps, hold it there. You drive milestone-by-milestone from your board, and you'll test the dashboard first (step 3 below).

2. In Claude Code, ask Claude to explain what it created, then to show you one change in full:

   ```
   What files did you create, and what does each one do? Then show me the
   diff for app.py and walk me through it.
   ```

   Read the diff, not only the explanation. If a line doesn't make sense, ask about it. If you'd have done something differently, say so and let Claude change it. That's a code review in miniature. Reading what the agent wrote, one file per milestone, is how you stay the person who knows what's in the project. The alternative is treating the AI's work as a black box.

3. Test the dashboard. Claude set up the `venv/` virtual environment while implementing TASK-1, so it's ready to use (if it isn't there for any reason, Claude will create it). In Claude Code:

   ```
   Stop any running Streamlit server, then activate my virtual environment
   and run the Streamlit app so I can test it.
   ```

   > **Key Concept: Virtual Environments.** A **virtual environment** (the `venv/` folder) is an isolated Python installation specific to this project. Without it, packages you install might conflict with other Python projects on your machine. It keeps your dashboard's dependencies (Streamlit, Pandas, Plotly) contained within this project. That's what "activate my virtual environment" asks for: use this project's Python, not the machine-wide one. If you ever run the app yourself in VS Code's terminal, activate it first with `source venv/bin/activate` (macOS) or `venv\Scripts\activate` (Windows), then `streamlit run app.py`; you'll see `(venv)` at the start of the prompt while it's active.

4. Claude starts the server and reports the **Local URL**, for example `http://localhost:8501` (the port number can differ if something else on your machine is already using that one). Open whatever URL it gives you: hold `Cmd` (macOS) or `Ctrl` (Windows) and click the link, or copy it into your browser. You should see the beginnings of your dashboard: likely a title and confirmation that the data loaded.

   The prompt starts with "stop any running Streamlit server" for a reason. Claude leaves the server running in the background after you test. A server that's already running doesn't pick up everything Claude adds in later milestones. Stopping it first means every test shows the code as it is now, so you can reuse this exact prompt after each milestone.

**Checkpoint:** The dashboard runs locally at the Local URL Claude reported, without errors.

### 4.2 Commit, push, and update TASKS.md

Now you'll save your work using Git and create a traceable link between your code and the task it fulfills. This three-step process (commit, push, update) is the basic rhythm of professional development.

#### Understanding Git's workflow

Git tracks your code changes through a series of stages. Understanding these stages prevents confusion about where your changes "live" at any point:

```
┌─────────────┐    git add    ┌─────────────┐   git commit   ┌─────────────┐
│  Your edits │ ───────────> │   Staging    │ ─────────────> │  Local repo │
│  (working   │              │    Area      │                │  (history)  │
│   directory) │              │              │                │             │
│             │              │  "Ready to   │                │  "Saved     │
│  Files you  │              │   be saved"  │                │   snapshot" │
│  changed    │              │              │                │             │
└─────────────┘              └─────────────┘                └─────────────┘
                                                                   │
                                                              git push
                                                                   │
                                                                   v
                                                            ┌─────────────┐
                                                            │   GitHub    │
                                                            │  (remote)   │
                                                            │             │
                                                            │  "Backed up │
                                                            │   & shared" │
                                                            └─────────────┘
```

Here is what each stage means:

- **Working directory:** the files on your computer as you edit them. Changes here aren't yet tracked by Git.
- **Staging area:** a holding zone for changes you intend to include in your next commit. The `git add` command moves changes here. This is like placing items in a box before sealing it.
- **Local repository:** your project's history of saved snapshots. The `git commit` command creates a new snapshot from everything in the staging area. Each snapshot is permanent and can be revisited.
- **Remote (GitHub):** the cloud copy of your repository. The `git push` command uploads your local commits to GitHub, making them visible to others and serving as a backup.

> **Key Concept: Traceability Through Commit Messages.**
> When you include the milestone ID (like TASK-1) in your commit message, you create a traceable link that connects your code change to the milestone that prompted it:
>
> ```
> TASK-1 in TASKS.md --> Commit "TASK-1: set up project and data loading" --> GitHub --> Deployed Dashboard
> ```
>
> A milestone may span more than one commit (executing-plans commits each plan step as it builds). What matters is that its commits carry the milestone ID and the board records where the work landed. Because `TASKS.md` is versioned too, `git log -- TASKS.md` then shows the full history of how milestones moved from To Do to Done. In professional environments, this traceability is how teams maintain accountability, conduct code reviews, and audit changes.

#### Steps

1. **Verify the milestone's commits.** As it worked through the milestone, executing-plans committed each plan step along the way, so there's usually nothing left to commit by the time you get here. This step is a check, not busywork: you're confirming the work is saved, the commits carry the milestone ID, and junk like `venv/` stayed out of the repo. In Claude Code:

   ```
   Is everything for TASK-1 committed, with the milestone ID in the commit
   messages? Commit anything still outstanding, and confirm venv/ is
   covered by .gitignore.
   ```

   Two outcomes, both fine: Claude reports it's all already committed (the usual case), or it commits the stragglers. Either way you end with a clean working tree and TASK-1's history in Git. You'll also notice two lines at the bottom of every commit message, `Co-Authored-By: Claude ...` and `Claude-Session: ...`. Claude Code adds them on its own. They're the agent signing its work, and they're fine to leave.

   > **Key Concept: .gitignore.** The `.gitignore` file tells Git which files and directories to ignore. Virtual environments (`venv/`), compiled files, and operating system files should never be committed to a repository; they're large, machine-specific, and can be regenerated. The `.gitignore` file prevents accidental commits of these files.

   > **What is a commit hash?** Each commit gets a unique identifier called a **commit hash**, a string like `05a9ada`. It's a fingerprint: no two commits in your repository will ever share one. A milestone may produce several commits; you'll record the last code commit on the milestone's **Commit:** line in `TASKS.md` so anyone can find the code that fulfilled it.

2. **Push, then update your board and push again.** One prompt does both. It uploads the milestone's commits, then records the result on the board and pushes that too, so the board on GitHub never trails the code. Claude sometimes moves a milestone to Done on its own while committing; this prompt makes sure the rest of the record (checked criteria, commit hash) is there too. In Claude Code:

   ```
   Push my changes to GitHub. Then update TASK-1 in TASKS.md: check off its
   acceptance criteria, put the hash of its last code commit on the Commit
   line, add a Notes line with anything Claude got wrong or that I changed
   (or "clean" if nothing), and move it to Done. Commit TASKS.md with a
   message like "TASK-1: mark done on the board" and push again.
   ```

   If this is your first push on the feature branch, Claude may need to set the upstream tracking branch. It handles this automatically.

3. **Verify on your board.** Open `TASKS.md` in VS Code. TASK-1 should now sit in the Done section looking roughly like this, with the hash of its last *code* commit on the Commit line (not the hash of the board update you just made):

   ```markdown
   ## Done
   - [x] **TASK-1: Project setup and data loading**
     - [x] App runs with `streamlit run app.py` and shows a title
     - [x] Loads `data/sales-data.csv`; handles a missing file cleanly
     - Commit: 05a9ada
     - Notes: imported plotly.express and never used it, removed
   ```

   The Notes line is your record of what needed a human. One line is enough: a wrong assumption, a change you asked for after reading the diff, or "clean." Those lines feed `CLAUDE.md` in Section 4.4, and they're the best material you'll have for the walk-through.

4. **Check your name on GitHub.** Open your repository in the browser, switch to the `feature/sales-dashboard` branch, and open the commit list (the **Commits** link near the top of the file list). Your avatar and username should appear beside each commit. If you see a grey placeholder instead, the email you set in Part 1 with `git config` doesn't match an email on your GitHub account. Until it does, none of your work shows on your profile. Add that email under GitHub **Settings** --> **Emails**, or rerun the `git config --global user.email` command with the right address. The fix applies to every commit from then on.

**Checkpoint:** Code and the updated board are on GitHub. TASK-1 is in the Done section of `TASKS.md` with its criteria checked and a commit on its Commit line, the history of `TASKS.md` (ask Claude to show it) includes the board commit for TASK-1, and your avatar shows on the commits on GitHub.

### 4.3 Complete remaining milestones

Now repeat the cycle for each remaining milestone on your board, in order. If one of your milestones is deployment, skip it for now; that comes in Section 5.

Before you start TASK-2, press **Shift+Tab** to switch to **Auto** mode (see the modes at the top of this section). From here Claude runs without asking, and your job shifts from approving each move to reading what it reports.

The cycle for each milestone is:

```
Take the next milestone, in a fresh conversation (/clear)
        |
        v
"Let's work on TASK-N" --> Move to In Progress --> executing-plans works its plan steps
        |
        v
Test the dashboard (ask Claude to run it)
        |
        v
Verify the milestone's commits carry the milestone ID
        |
        v
Push --> update TASKS.md (check off, Commit line, move to Done) --> push the board
```

Here is the pattern for each milestone. Start it in a fresh conversation. In Claude Code:

```
/clear
```

Then send the milestone prompt, with your own plan's file name after the `@` (type `@docs/` and let the autocomplete finish it):

```
Let's work on TASK-2. Move it to In Progress in TASKS.md, then implement
the plan steps it covers, inline in this session (no subagents). The
plan is in @docs/superpowers/plans/2026-09-08-sales-dashboard.md.
```

> **Why a fresh conversation for each milestone?** Claude re-reads the whole conversation on every step it takes. By the third milestone that's well over a hundred thousand words, most of them about work that's already finished. Every step then costs more of your usage allowance than it did in a short session. Claude Code will tell you so itself, with a "/clear to save ..." note in the status bar. Nothing is lost by clearing: the plan, the board, and the code are files on disk, and the prompt points Claude at the plan. The same prompt is how you pick up tomorrow in a new terminal. Two parts of it exist only because the conversation is new. "Inline in this session" keeps Claude from handing each task to a subagent, which Superpowers does by default when nobody has said otherwise. The plan's path tells it where to look.

Claude auto-invokes `executing-plans` and works through the plan steps under the milestone. When it finishes, ask for the diff of one file and read it, as you did in 4.1. Then run the app with the same prompt as 4.1 step 3 to see the new piece on screen.

After implementation and testing, run the same check-and-push as in 4.2. Claude usually updates the board on its own as it finishes a milestone, so this comes back as a confirmation more often than a change. In Claude Code:

```
Verify everything for TASK-2 is committed with the milestone ID and commit
anything still outstanding. Push to GitHub. Then update TASK-2 in
TASKS.md: check off its acceptance criteria, put the hash of its last
code commit on the Commit line, add a Notes line with anything Claude got
wrong or that I changed (or "clean"), and move it to Done. Commit that
board update and push it too.
```

> **Now loop until the board is done.** The prompts above show TASK-2, but this cycle is the rest of your build: run it again for TASK-3, then TASK-4, and every remaining implementation milestone, swapping in the current milestone ID each time. You're finished with this section only when every implementation milestone sits in the Done section of `TASKS.md`. One prompt pair per milestone; don't stop after TASK-2.

> **Handy: accept Claude's next-prompt suggestions.** As you repeat this cycle, Claude Code often shows a dimmed suggestion in the input box, its guess at what you might type next (like committing, or starting the next milestone). Press the **right arrow** (or **Tab**) to drop it into your prompt, then **Enter** to send it. To write your own instead, just start typing and the suggestion disappears. It's on by default; you can turn it off in `/config` if you find it distracting.

> **Leave the deployment milestone in To Do (if you have one).** The plan's deployment step is gated on you: you marked it as yours in the Section 2.2 prompt, so this build loop covers the implementation milestones only. Claude may still offer to start deployment for you; if it does, or if it has already moved the milestone to In Progress, hold the gate:
>
> ```
> Deployment is my step. Move that milestone back to To Do; I'll run it
> from main after we merge.
> ```
>
> This is the ground rule from Section 2.2 in action: the AI builds, but you decide when your work goes live.

> **Pro Tip:** Watch Claude's output as it works each milestone. You'll see files being created, imports being added, and functions being written. This is a good way to learn how professional code is structured. Pay attention to how Claude names variables, organizes functions, and handles data. You can reuse these patterns in your capstone.

After working through all implementation milestones, test the complete dashboard one final time. In Claude Code:

```
Stop any running Streamlit server, then activate my virtual environment
and run the Streamlit app so I can test the complete dashboard.
```

Open whatever Local URL Claude reports (for example `http://localhost:8501`). Then open the PRD's **Acceptance Criteria** section beside it and check each item against what's on screen, yourself, without asking Claude. The PRD's **Expected Output** table gives you the numbers to look for: total sales near $116,500 and 482 orders. Passing tests prove the functions return what the tests asked for. They don't prove the chart is the right chart, the bars are sorted the way the PRD says, or the page would pass in an executive meeting. That's what your eyes are for. Anything that fails goes back to Claude as a plain request ("the region chart isn't sorted largest to smallest, fix it and commit under TASK-4") before you move on.

**Checkpoint:** All implementation milestones are in the Done section of `TASKS.md` with their criteria checked and a commit on each Commit line, the history of `TASKS.md` (ask Claude to show it) has at least one board commit per finished milestone, and every PRD acceptance criterion checks out on the running app. Only a deployment milestone (if you have one) remains in To Do.

### 4.4 Capture project memory with /init

Your dashboard is built and working, so now is the moment to give your project a memory. You'll generate a `CLAUDE.md`, a file Claude Code reads at the start of every session, so future sessions (and your capstone) begin with context instead of a blank slate.

> **If Claude showed you a menu after your last milestone:** hold off. After the final plan step, Superpowers sometimes runs your whole test suite and offers three choices (the `finishing-a-development-branch` step). They are merge to main locally, push and create a pull request, or keep the branch as it is. The menu doesn't always appear. If it does, don't pick yet. Do this `/init` step first so `CLAUDE.md` is part of the merge, then handle the menu in Section 4.5.

> **What is CLAUDE.md, and why now?** `CLAUDE.md` documents your project for the AI: how to run it, where the key files live, the conventions you follow. Claude Code's `/init` command writes one for you by scanning your code. That's why you do it *now* and not at the start: at the start there's nothing to describe; now it can capture your actual project. It also pays off on a team: because `CLAUDE.md` is committed to the repo, every teammate's Claude Code session reads the same file, so everyone (and their AI) follows the same setup, conventions, and structure. That keeps development consistent, and a new teammate gets up to speed from one file instead of asking around.

1. In Claude Code, run:

   ```
   /init
   ```

2. Claude scans your project and writes `CLAUDE.md` to the repo root. Open it in VS Code and read it; it should describe your dashboard: how to run it (`streamlit run app.py`), the main files, and where the data lives. Fix anything that's off, or ask Claude to adjust it.

3. Add what you learned, then commit. The Notes lines on your board are a list of things that needed a human. Turned into rules, they keep the next session from repeating them. In Claude Code:

   ```
   Add a short "Lessons" section to CLAUDE.md built from the Notes lines in
   TASKS.md, written as rules for future sessions. Then commit CLAUDE.md
   with the message "Add project memory (CLAUDE.md)".
   ```

   This is how experienced people use these files. Mitchell Hashimoto, who runs a large open-source project with coding agents, says each line of his instructions file "is based on a bad agent behavior." Yours starts the same way, from the mistakes you caught today.

> **Claude's own notes.** Alongside `CLAUDE.md`, Claude Code keeps notes it writes for itself, called **auto memory**, in a folder under your home directory rather than in the repo. That's what "Saved 2 memories" means when you see it. The difference: `CLAUDE.md` is what you tell Claude about the project, and it ships with the repo to anyone who clones it. Auto memory is what Claude noticed on its own, and it stays on your machine. You can read or delete those notes any time with `/memory`.

> **For your capstone:** run `/init` once you have a skeleton of the project, then keep `CLAUDE.md` updated as the project grows. Every new Claude Code session then starts already knowing your project.

**Checkpoint:** `CLAUDE.md` exists at the repo root, describes your dashboard, and is committed.

### 4.5 Review, then merge to main

Your feature branch contains all the implementation work. Before it becomes the official version of the code, you'll review it, the way a teammate would review yours. Then you'll bring it into `main`.

> **Key Concept: Merging.**
>
> ```
> main:          A --- B --- C ─────────────── D (merge commit)
>                             \               /
> feature:                     E --- F --- G -
> ```
>
> Your feature branch diverged from `main` at point C. You then made commits E, F, and G on the feature branch. Merging creates a new commit (D) on `main` that incorporates all the changes from the feature branch. After the merge, `main` contains everything: the original code plus all your dashboard work.
>
> This is why feature branches are valuable; they let you develop freely without risking the stable `main` branch. When you're confident your work is complete, you merge once and know that `main` stays reliable.

1. **Confirm your branch and a clean slate.** In Claude Code:

   ```
   Which git branch am I on, and are there any uncommitted changes?
   ```

   You should be on your feature branch (e.g., `feature/sales-dashboard`) with nothing uncommitted. If Claude finds stray changes (a leftover `TASKS.md` edit is the usual suspect), have it commit them now, with their own message, rather than letting them tangle into the merge. Claude tends to run this same check on its own before merging; now you know why.

2. **Review the branch.** Every team reviews code before it lands on `main`, and an agent's code is no exception. You own what you ship, and this is the moment to find out what that is. Claude Code has a built-in review. In Claude Code:

   ```
   /code-review feature/sales-dashboard
   ```

   Claude reads every change on the branch and returns a list of findings with the most serious first: a bug, a missing check, code that does the same thing twice, a name that misleads. (If it says there's nothing to review, ask in plain English instead: *Review every change on this branch compared with main and list the problems, ranked by how much they matter.*) Read the list. For each finding, decide: fix it, or leave it and know why. Then tell Claude what you decided, for example:

   ```
   Fix the first and third findings. Leave the second one, the PRD doesn't
   ask for that. Commit the fixes with the message "Review fixes".
   ```

   > **Why you decide, not Claude.** A reviewer's job is to find things. Yours is to weigh them against what the project needs. Some findings are real bugs. Some are style. Some are the reviewer being thorough about something the PRD never asked for. Sorting those apart is the judgment this tutorial is trying to grow, and the walk-through will ask what the review found and what you did about it. The list is in your conversation, and your decision is in the fix commit.

3. **Merge into main.** If the three-option menu from the end of your last milestone is still waiting (the one you held off on in Section 4.4), pick option 3, keep the branch as it is, so you can do the merge in your own words. In Claude Code:

   ```
   Merge feature/sales-dashboard into main with a merge commit (no
   fast-forward), so the branch shows in the history.
   ```

   Claude switches to `main`, merges the feature branch, and reports the result.

   > **Why ask for a merge commit?** Left to itself, Git takes a shortcut when it can. If `main` hasn't changed since you branched, it moves the `main` label forward to your last commit and creates no merge commit at all. Your history then looks as if the branch never existed. Someone reading your repo, your instructor say, can't tell that apart from working on `main` the whole time. Asking for a merge commit gives you the commit D in the diagram above, with the branch visible underneath it.

4. **Push main to GitHub.** In Claude Code:

   ```
   Push main to GitHub
   ```

5. **Verify on GitHub:** Open your repository in a browser (`github.com/[your-username]/[your-repo]`). Just above the list of files, on the left, is a button showing the current branch name with a small branch icon next to it. Click that button and choose **main** from the dropdown (it may already be selected). Then confirm all the dashboard files are in the file list: `app.py`, `requirements.txt`, the `data` directory, and so on.

**Checkpoint:** The `main` branch on GitHub contains all your dashboard code.

---

## Section 5: Deploy (~15 min)

### Why deployment matters

> **Why This Matters:** Building something that only runs on your laptop doesn't deliver value. Deployment makes your work accessible to stakeholders: a manager, a client, or your capstone advisor can open a URL and see your dashboard without installing Python or cloning a repository. Going from analysis to a shared, accessible output is a skill most graduates lack. Many people can build charts in a Jupyter notebook; far fewer can deploy an interactive dashboard that stakeholders actually use.

Deployment is the final stage of the professional workflow. It transforms your local project into a publicly accessible application. It's also the handoff you reserved back in Section 2.2: the plan's final step, marked as yours, executed here by you.

```
┌──────────────┐     Streamlit     ┌──────────────┐     Public URL    ┌──────────────┐
│  Your code   │ ──── Cloud ────> │  Cloud server │ ───────────────> │  Stakeholders│
│  on GitHub   │     reads your   │  runs your    │    anyone with   │  view your   │
│  (main branch)│    code         │  app.py       │    the URL       │  dashboard   │
└──────────────┘                  └──────────────┘                   └──────────────┘
```

### 5.1 Deploy to Streamlit Cloud

Streamlit Community Cloud is a free hosting service specifically designed for Streamlit applications. It reads your code directly from GitHub and runs it on their servers.

> **Prerequisite:** Your code must be merged to `main` (Section 4.5) before deploying. Streamlit Cloud deploys from the `main` branch by default.

1. Go to [share.streamlit.io](https://share.streamlit.io) in your browser.

2. Click **Continue to sign-in** on the landing page, then click **Continue with GitHub** and authorize Streamlit to access your repositories.

   > **First-time sign-in:** If this is your first time using Streamlit Cloud, the process involves a few extra steps after clicking "Continue with GitHub":
   > - You'll authorize Streamlit on GitHub (email-only permissions), then **verify your email** by entering a 6-digit code sent to your email address.
   > - After verification, you'll authorize Streamlit a second time with broader GitHub permissions (repository access, webhooks).
   > - Finally, you'll fill out a short account setup form: name, functional area (choose **Student**), development stage, and country. Click **Continue** to finish.
   >
   > On subsequent sign-ins, you'll skip straight to the dashboard.

3. Click **Create app** in the top-right corner, then select **Deploy a public app from GitHub** on the next page.

4. Configure the deployment:

   | Field | Value |
   |-------|-------|
   | **Repository** | `[your-username]/ai-dev-workflow-tutorial` |
   | **Branch** | `main` |
   | **Main file path** | `app.py` (or wherever your Streamlit entry point is) |
   | **App URL** (optional) | A custom slug like `sales-dashboard-yourname`; this determines the first part of your public URL |

5. Click **Deploy** and wait 1-2 minutes. Streamlit Cloud installs your dependencies (from `requirements.txt`), runs your app, and makes it available at a public URL.

6. When deployment completes, you receive a URL like:

   ```
   https://sales-dashboard-yourname.streamlit.app
   ```

   Open this URL and verify that your dashboard looks and functions the same as it did locally.

> **If deployment fails:** The most common cause is a missing or incorrect `requirements.txt`. Check that the file exists in your repository's `main` branch on GitHub and lists all required packages (streamlit, pandas, plotly, etc.). If it's missing, ask Claude to create one, commit, push, and redeploy. A second cause: if a `uv.lock`, `Pipfile`, or `pyproject.toml` found its way into the repo, Streamlit Cloud reads those before `requirements.txt`. Ask Claude to remove them, commit, and push, then redeploy.

### 5.2 Update your task board

Record the deployment on your board. Give Claude the live URL and let it finish the bookkeeping. In Claude Code:

```
The dashboard is live at [paste your URL]. Record the URL next to the
deployment milestone in TASKS.md (add the milestone if it's missing),
check off its criteria, and move it to Done. Add the same URL near the
top of README.md. Then commit both files and push main to GitHub.
```

The README line matters: it's the first thing your instructor, or anyone else who opens the repo, sees.

You're on `main` now (the merge in Section 4.5 switched you there), so this last update commits straight to `main`. Pushing it makes your finished board visible on GitHub, which is what your instructor checks.

**Checkpoint:** The dashboard is live and accessible at a public URL. The deployment milestone is in the Done section of `TASKS.md` with the live URL recorded, and the update is pushed to GitHub.

---

## Section 6: Final verification checklist

Before submitting, walk through every item below. Each category corresponds to a section of this guide.

### Superpowers artifacts

- [ ] Design document created (`docs/superpowers/specs/<file>.md`)
- [ ] Implementation plan created (`docs/superpowers/plans/<file>.md`)

### Task board (TASKS.md)

- [ ] Milestones created from the PRD (4-8 of them: TASK-1, TASK-2, ...), each with acceptance criteria
- [ ] A Definition of Done applies to every milestone
- [ ] All implementation milestones are in the Done section, criteria checked
- [ ] Each done milestone has a commit hash on its Commit line
- [ ] The live URL is in `TASKS.md` and near the top of `README.md`

### Dashboard

- [ ] Runs locally with KPIs, line chart, and bar charts
- [ ] Deployed and publicly accessible on Streamlit Cloud

### Version control

- [ ] Commits include milestone IDs (TASK-1, TASK-2, ...) in messages
- [ ] `CLAUDE.md` generated with `/init`, with a Lessons section, and committed
- [ ] Branch reviewed with `/code-review` before the merge, and the fixes you chose committed
- [ ] Feature branch merged to main
- [ ] All code pushed to GitHub on the main branch

---

## Section 7: Turn in your work

Every item above checked? Then you're done building, and the last step is turning it in.

Several courses use this tutorial, and each sets its own deadline and its own submission channel. Your course tells you where and when. What follows is what you need to have ready.

1. **GitHub repository link:** your public repo URL (e.g., `https://github.com/yourusername/ai-dev-workflow-tutorial`)

2. **Streamlit dashboard link:** your live deployed URL (e.g., `https://sales-dashboard-yourname.streamlit.app`)

3. **Your completed `TASKS.md`:** because the board lives in your repo. Just make sure the final `TASKS.md` on your `main` branch shows:
   - Every implementation milestone in the Done section, acceptance criteria checked
   - A commit hash on each done milestone's Commit line
   - The deployment milestone done, with the live URL recorded

   Your instructor can open `TASKS.md` on GitHub and run `git log -- TASKS.md` to see how the work progressed, and that history is your evidence.

Make sure your `TASKS.md`, `prd/`, and `docs/superpowers/` files are included in your repository.

**Checkpoint:** your repo opens on GitHub, your dashboard loads at its public URL, and both links have gone wherever your course asks for them.

Whatever your course's grading looks like, here is what an instructor can see from the repo alone. Each item is a step in this guide, so if you did the steps, the evidence is there.

- The spec and plan committed before the first code commit
- A TASK id on every implementation commit
- A Commit line and a Notes line under every milestone
- A Lessons section in `CLAUDE.md`
- A review-fix commit before the merge
- A merge commit with the branch visible under it

> **If your course includes a 1:1, the walk-through comes next.** Handing in the links isn't the last step, explaining the work is. You'll walk your instructor through what you built and how, live. Expect these four prompts, the same for everyone:
>
> 1. Pick one file Claude wrote and explain a diff from it, line by line.
> 2. Name one test in `tests/` and say what would break if it were deleted.
> 3. Take one requirement from the PRD and trace it to a milestone on your board and to the commit that delivered it.
> 4. Tell the story of one Notes line: what Claude got wrong, how you caught it, and what changed.
>
> Follow-ups will come from your own repo. Why did the work happen on a feature branch? What did the design doc change about what you built? What did the code review find, and what did you do about it? Why did the merge come before the deploy? This isn't a quiz to cram for, and it isn't a hunt for AI use (AI was expected everywhere in this tutorial). It checks the one thing a polished repo can't show: that the reasoning behind it is yours. Your prep material is already on the record. Reread your spec, your plan, your board with its Notes lines, and your commit history, and make sure you can tell the story of each out loud with the tool closed. If you can, you're ready, both for this meeting and for the capstone, where you'll do the same thing in front of stakeholders.

---

## The complete workflow: what you accomplished

```
PRD [done] -> TASKS.md [done] -> brainstorming [done] -> writing-plans [done] -> Code [done] -> Commit [done] -> Push [done] -> Deploy [done] -> Live! [done]
```

In this guide, you practiced five professional skills:

1. **Skill-driven development:** You brainstormed, planned, broke down tasks, then implemented. This discipline works with any technical project, not just this tutorial.

2. **AI-assisted coding:** You used Claude Code as a tool guided by clear specifications. You saw how context engineering (the `@` symbol, CLAUDE.md, slash commands) makes AI assistance more precise.

3. **Task tracking in your repo:** Every piece of work was tracked from To Do to Done in `TASKS.md`, with each task linked to the commit that fulfilled it.

4. **Version control with Git and GitHub:** You created feature branches, committed with meaningful messages, pushed to a remote, and merged completed work.

5. **Deployment:** You turned a local script into a live application with a shareable URL.

> **For Your Career:** This workflow scales. Whether you're building a data pipeline, a dashboard, or a machine learning model, the pattern is the same: brainstorm, plan, track, build, deploy. You now have hands-on experience with the full cycle. In interviews, you can describe not just what you built but how you built it, and that process awareness matters to hiring managers.

---

## Troubleshooting

Something will break: a command won't run, the app won't start, a push gets rejected. That's normal, and you already have the best debugging tool installed: Claude Code.

**Ask Claude Code first.** It can see your project, read the error, run commands to investigate, and usually fix the problem for you. Give it the specifics:

- Paste the **exact** error message; don't paraphrase it.
- Say what you were trying to do and what you expected to happen.
- If the first fix doesn't work, paste the new error and let it try again.

For example:

```
I ran `streamlit run app.py` and got this error:
<paste the full error here>
What's wrong and how do I fix it?
```

This handles the large majority of what goes wrong here: wrong file paths, a missing package, a port already in use, a rejected push, a merge conflict. Let Claude diagnose before you go hunting through documentation.

**Three habits that fix things before you even ask:**

- **Read the error.** It usually names the problem, and sometimes the fix.
- **Open a new terminal.** This alone clears most "command not found" errors right after you install a tool.
- **Check where you are.** Run `pwd`; Git and Streamlit commands only work inside your project folder.

**Still stuck?** Post in the Teams General channel, or send me a direct message on Teams, with what you were doing, the exact error, and what you already tried. Someone will help.

---

## Other Superpowers skills you'll meet later

You'll encounter these in larger projects beyond this tutorial. We didn't formally use them here either because they're more advanced than this project needs, or because we explicitly told the skill not to (in the brainstorm prompt).

| Skill | What it does | Why we skipped it here |
|-------|--------------|------------------------|
| `using-git-worktrees` | Creates an isolated working directory per branch so multiple branches can be checked out at the same time | We told brainstorming to skip it (in the prompt) to keep this project on a single working directory |
| `dispatching-parallel-agents` | Splits independent tasks across multiple agents that work in parallel | Overkill for a single-project tutorial |
| `subagent-driven-development` | Runs a plan by handing each task to a fresh subagent and reviewing the result before the next | Superpowers' recommended way to run a plan, and the one you'll likely use on a capstone. You chose inline in 2.2 so you could watch the build |
| `writing-skills` | Helps you author your own Superpowers skills | Meta. For skill authors, not skill consumers |
| `systematic-debugging` | Walks through a structured debugging process when something breaks | Triggers automatically if your build hits an unexpected error |

If you want to dig deeper, browse the Superpowers skill library: https://github.com/obra/superpowers-skills

---

## Glossary

Quick-reference table of key terms used in this document.

| Term | Definition |
|------|------------|
| **Acceptance Criteria** | The specific, checkable conditions a single milestone must meet to count as complete |
| **brainstorming** | A Superpowers skill that asks clarifying questions about a proposed feature and produces a design document |
| **Branch** | A separate line of development in Git, allowing isolated work without affecting the main codebase |
| **Commit** | A saved snapshot of your project at a specific point in time, like a version you can return to |
| **Commit Hash** | A unique identifier (e.g., `05a9ada`) assigned to each commit, serving as its permanent fingerprint |
| **Definition of Done** | A shared standard that must hold before any milestone moves to Done, on top of each milestone's own acceptance criteria |
| **Deploy** | Make software accessible on a server so users can reach it via a URL |
| **executing-plans** | A Superpowers skill that implements tasks from an implementation plan one at a time, with frequent commits |
| **Feature Branch** | A branch created specifically for developing one feature, separate from main |
| **Template repository** | A GitHub repository you can copy into a new repository of your own, with a fresh history and no link back to the original |
| **Implementation plan** | The detailed, step-by-step build list `writing-plans` produces in `docs/superpowers/plans/`; Claude builds from it |
| **Merge** | Combine changes from one branch into another, integrating completed work |
| **Milestone** | A coarse, human-facing deliverable on your `TASKS.md` board (TASK-1, TASK-2, ...) that groups several plan steps |
| **PRD** | Product Requirements Document, a written description of what to build and why |
| **Push** | Upload local commits to a remote repository (GitHub), making them visible and backed up |
| **Staging Area** | A holding zone in Git for changes you intend to include in your next commit |
| **Streamlit** | A Python library that transforms Python scripts into interactive web applications |
| **Superpowers** | A Claude Code plugin that gives Claude a library of skills (brainstorming, writing-plans, executing-plans, and more) |
| **TASKS.md** | A Markdown file in your repository that tracks every milestone through To Do, In Progress, and Done |
| **Traceability** | The ability to link code changes back to the requirements that prompted them |
| **venv** | Virtual environment, an isolated Python installation that keeps project dependencies separate |
| **writing-plans** | A Superpowers skill that turns a design document into a bite-sized implementation plan |
| **.gitignore** | A file that tells Git which files and directories to exclude from version control |

---

## What's next

You now have a complete professional workflow you can apply to your capstone project and beyond. The same cycle (brainstorm, plan, track, build, deploy) works for any technical project, whether it's a data pipeline, a machine learning model, or another dashboard. The tools and habits transfer.

> **Can you explain it without Claude in the room?** Getting the dashboard to run is the easy half. The real test is whether you can walk someone through what you built and why, and defend the decisions, with the AI closed. That's what your capstone will ask of you: in advisor check-ins, stakeholder meetings, and presentations, you speak the reasoning, not just show the result. Practice it now: out loud, explain your spec, your plan, and one tradeoff you made. Any part that comes out fuzzy is the part to go back and understand, because the tools and the process here are yours to account for.

> **For your capstone: meetings and dictation.** Two more tools pay off once you're working with real stakeholders. Granola is an AI notepad that records your meetings and can hand the notes to Claude Code. You can then ask *"From this week's meeting notes, what did the client ask us to change?"* Wispr Flow is dictation, for giving Claude a few paragraphs of context by voice instead of typing them. Neither is needed for this tutorial. Both are in the [capstone tools appendix](capstone-tools.md), with the student plans and setup steps.
