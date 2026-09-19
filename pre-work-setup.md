# Part 1: Setup & Foundation

**Get your tools set up before you start building (Part 1 of 2)**

Estimated time: 55–80 minutes, at your own pace. Do this part first; Part 2 (Build & Deploy) picks up where it leaves off.

---

## Table of contents

- [Section 1: Create accounts (~15 min)](#section-1-create-accounts-15-min)
  - [1.1 GitHub account](#11-github-account)
  - [1.2 Claude Pro subscription](#12-claude-pro-subscription)
- [Section 2: Install tools (~40 min)](#section-2-install-tools-40-min)
  - [2.1 VS Code](#21-vs-code)
  - [2.2 Git](#22-git)
  - [2.3 Python 3.11+](#23-python-311)
  - [2.4 Claude Code](#24-claude-code)
  - [2.5 Superpowers plugin](#25-superpowers-plugin)
- [Section 3: Create your repository and clone it (~15 min)](#section-3-create-your-repository-and-clone-it-15-min)
  - [3.1 Create your repository](#31-create-your-repository)
  - [3.2 Clone your repository](#32-clone-your-repository)
- [Section 4: Final verification (~10 min)](#section-4-final-verification-10-min)

---

## What you'll set up

```
Accounts:  GitHub, Claude Pro
Tools:     VS Code, Git, Python 3.11+, Claude Code, Superpowers plugin
Repo:      Your own copy of the tutorial repository, created from the template and cloned
Tracking:  A TASKS.md file you create in Part 2 (no extra account needed)
```

**See the finished product:** Before you start, look at what you'll build in Part 2: [E-Commerce Sales Dashboard](https://sales-dashboard-greg-lontok.streamlit.app/). This is a live, deployed dashboard built using the workflow you're about to learn. By the end, you'll have built and deployed your own version. (Free Streamlit apps go to sleep after 12 hours without visitors. If you land on a sleeping page, click **Yes, get this app back up!** and wait about 30 seconds.)

> **Already paying for ChatGPT?** It includes OpenAI's Codex, a coding agent that does the same job as Claude Code, and this tutorial's workflow runs on either. Don't buy a second subscription. Skip Section 1.2, and at the points marked in the [Codex companion](codex-companion.md) (installing the agent, the plugin, and a few commands in Part 2) follow the companion instead. Everything else here applies to you as written.

> **If you get stuck:** Try to work the problem yourself first, that's the skill you're building. Two fixes solve most setup issues: read the error message (it usually names the problem), and open a new terminal (that alone clears most "command not found" errors right after you install a tool). The one exception is `claude`: if that's the missing command, follow the installer's setup notes in Section 2.4, Step 2. If those don't do it, search the exact error, or once Claude Code is set up, paste the error and ask it to diagnose. Still stuck? Post in the Teams General channel, or send me a direct message on Teams, with what you were doing, the exact error, and what you already tried.

> **Heads up:** Websites and software update their interfaces regularly. A button label, sign-up flow, or menu option described here may look slightly different by the time you go through it. That's normal. Focus on the goal of each step rather than the exact clicks: once you know what a step is trying to accomplish, you can usually find the equivalent option even when the UI has moved. Read the screen, work it out, and keep going. Figuring things out on your own like this is itself a professional skill.

---

## Why this setup matters

Setting up your own development environment is a skill most people skip. They wait for someone else to do it for them. When you can configure a toolchain yourself, debug installation problems, and get everything running from scratch, teammates and managers notice. It tells them you can own a problem from start to finish.

A well-configured environment also saves you time. Every technology company uses some variation of the workflow you're about to configure. The tools differ slightly from team to team, but the pattern is the same:

```
Requirements  -->  Code  -->  Test  -->  Deploy  -->  Monitor
```

Someone defines what needs to be built. Developers write code to meet those requirements. The code is tracked, reviewed, and deployed so users can access it. This cycle repeats continuously.

You're setting up that same pipeline, end to end. When you finish, you'll have a development environment that looks like what you'd find on your first day at a technology job. This is also the environment you'll use for your capstone project, so getting it right now saves you time later.

### Your competitive advantage

Most analysts can build a model in a notebook. Fewer can turn that model into a live dashboard and deploy it. That gap is your opportunity, in your capstone and in job interviews.

### What you'll be able to do after Part 1

- Manage code with version control (Git and GitHub)
- Use AI to accelerate building (Claude Code)
- Plan before you build (Superpowers' brainstorming and writing-plans skills)
- Read and edit code in the editor most developers use (VS Code)

AI-assisted development doesn't replace understanding. It accelerates it. You still need to know what you're building and why. The AI handles much of the how.

---

## The complete toolchain

The following diagram shows every tool you'll install and how they connect. Refer back to this as you work through each section.

```
+-------------------------------------------------------------+
|               Your Development Toolchain                     |
+-------------------------------------------------------------+
|                                                              |
|  GitHub (code hosting)  <-->  Git (version control)          |
|       ^                           ^                          |
|       |                           |                          |
| TASKS.md (task tracking) <-->  VS Code (code editor)         |
|       ^                           ^                          |
|       |                           |                          |
| Claude Code (coding agent) <--> Superpowers (planning skills) |
|       ^                                                       |
|       |                                                       |
| Python + Streamlit                                           |
|  (your application)                                          |
|                                                              |
+-------------------------------------------------------------+
```

- **GitHub** stores your code in the cloud so it's safe, shareable, and versioned.
- **Git** is the version control engine that tracks every change you make.
- **TASKS.md** is a plain-text task board that lives in your repository. It tracks what to build and what's done, and because it's just a file, Claude Code can read and update it directly, with no separate account or web app to switch to. The board holds your milestones (the major deliverables, with IDs like TASK-1), and the plan you write in Part 2 breaks each milestone into the smaller build tasks Claude Code works through.
- **VS Code** is your code editor, where you read and organize files. Its built-in terminal is where Claude Code runs.
- **Claude Code** is an AI coding agent that runs in your terminal, reads your project, and helps you build.
- **Superpowers** is a Claude Code plugin whose skills (brainstorming, writing-plans, executing-plans) turn requirements into bite-sized implementation tasks before you start coding.
- **Python + Streamlit** is the technology stack for the dashboard you'll build in Part 2.

---

## Section 1: Create accounts (~15 min)

### 1.1 GitHub account

> **Why GitHub?** GitHub hosts over 100 million developers and is the standard platform for storing and collaborating on code. In your career, you'll use it to share code, collaborate on projects, and build a public portfolio. Recruiters check GitHub profiles.

**Steps:**

1. Go to [github.com](https://github.com) and click **Sign up**.
2. Choose a sign-up method: **Continue with Google**, **Continue with Apple**, or fill out the form manually with your email, a password, a username, and your country/region.
3. If signing up manually, check your email for a verification code and enter it when prompted. You may be asked to sign in again with your new credentials after verifying.
4. Complete any onboarding prompts if they appear (you may go directly to the dashboard).

**Username guidance:** Your GitHub username becomes part of your public profile URL (`github.com/your-username`). Choose something professional, like your name or a clean variation of it. Avoid numbers that look like birth years, inside jokes, or anything you wouldn't put on a resume. Letters, numbers, and single hyphens are the only characters allowed.

> **Checkpoint:** You can log into github.com and see your dashboard.

> **Pro Tip:** Your GitHub profile is a portfolio. The projects you build (in this tutorial, in your capstone, on your own) are all visible. A GitHub profile with well-documented projects shows employers you can build, not just analyze. Choose your username carefully. You'll use it for years.

---

### 1.2 Claude Pro subscription

> **Why Claude Pro?** Claude Code, the AI coding agent you'll use throughout this tutorial, requires an active Claude Pro (or Max) subscription. The free tier of Claude doesn't provide access to Claude Code. You need Pro to use the terminal-based AI assistant in this tutorial.

**Steps:**

1. Go to [claude.ai](https://claude.ai) and sign up using Google or email.
2. On the pricing page, click **Try Claude** under the **Pro** plan.
3. Enter payment information and complete the subscription ($17/month with annual billing, or $20/month billed monthly).

**A note about Pro vs. Max:** Most students find Claude Pro sufficient for this tutorial and their coursework. You only need the Pro subscription for one month to complete this tutorial. If you hit usage limits during intensive work sessions, Claude Max (from $100/month) provides higher limits. You can always upgrade later if needed. You can cancel your subscription after completing the tutorial, but it's highly recommended that you resubscribe when you start your capstone project; Claude Code is just as useful there. You can also apply what you learn here to other classes or your job if you're working.

**If the subscription cost is a concern,** message me on Teams. I don't want that to be a blocker for anyone.

> **What Pro gives you in Claude Code.** Pro includes two models. Sonnet 5 is the default and is plenty for everything in this tutorial. Opus 5 is stronger and slower, and you can switch to it inside Claude Code with `/model`, but it uses up your allowance faster. Pro has a 5-hour usage window and a weekly limit, shared between claude.ai and Claude Code. Run `/usage` inside Claude Code to see where you stand. When a limit resets, Claude Code picks up where it left off. One thing to leave alone: the **usage credits** setting on claude.ai. It's off by default, and turning it on lets fast mode and the Fable models bill you beyond your subscription. Nothing in this tutorial needs it.

> **Checkpoint:** When you're logged in to claude.ai, a Pro badge appears next to your name in the bottom-left corner.

---

## Section 2: Install tools (~40 min)

### Understanding your terminal

Before installing any tools, you need to understand the terminal, the interface where you'll run installation commands, interact with Git, and launch Claude Code.

> **What is a terminal?** A terminal (also called a command line or CLI) is a text-based interface where you type commands instead of clicking buttons. Professional developers use a terminal daily. It might feel unfamiliar at first, but by the end of this tutorial, you'll be comfortable with the essential commands. You don't need to memorize everything; Claude Code itself runs in the terminal and can help you with commands when you need it.

**Opening the terminal in VS Code:**

Once VS Code is installed (Section 2.1), you'll open the terminal inside it. Go to **Terminal** --> **New Terminal** from the menu bar, or use the keyboard shortcut `` Ctrl+` `` (backtick key, usually below Escape).

```
+-----------------------------------------------------------+
|  VS Code Window                                           |
|-----------------------------------------------------------|
|                                                           |
|  [Your code and files appear here]                        |
|                                                           |
|-----------------------------------------------------------|
|  Terminal                                            - x  |
|  $ _                                                      |
|                                                           |
+-----------------------------------------------------------+
```

You can resize the terminal by dragging the divider between it and the editor area.

**Essential terminal concepts:**

- **The prompt** (`$` on macOS/Linux, `>` on Windows) is the symbol that tells you the terminal is ready for your command. You don't type the prompt character itself; it's already there.
- **Running commands** follows the pattern: `command [options] [arguments]`. For example, `git --version` runs the `git` command with the `--version` option.
- **`pwd`** (print working directory) shows you where you are in the file system. Think of it as "where am I right now?"
- **`ls`** (list) shows the files and folders in your current directory. On Windows, use `dir` instead.
- **`cd foldername`** (change directory) moves you into a folder. `cd ..` moves you up one level.
- **Tab completion** is your best friend. Start typing a file or folder name, then press Tab. The terminal will autocomplete it. This saves time and prevents typos.
- **Ctrl+C** stops a running command. If something seems stuck or you made a mistake, press Ctrl+C to cancel.
- **Arrow keys**: Press the up arrow to recall previous commands. This is faster than retyping them.

> **Why open a new terminal after installing tools?** When you install a tool, it updates your system's **PATH**, the list of directories your computer checks when looking for programs. Terminals that are already open loaded the PATH when they started and don't automatically see updates. Opening a new terminal (Terminal --> New Terminal) loads the fresh PATH with the newly installed tool. This is the most common reason for "command not found" errors after installation.

You'll see reminders about this throughout the installation steps. If a tool doesn't seem to work after installing it, your first step should always be to open a new terminal.

One installer, Claude Code's, sometimes can't update the PATH for you. When that happens it prints the fix in its **Setup notes** at the end of the install, and you have to run or follow that note before a new terminal will help. Section 2.4 walks through it for macOS and Windows.

---

### 2.1 VS Code

> **What is VS Code?** Visual Studio Code (VS Code) is a free code editor from Microsoft and the most widely used one. You'll use it for two things. One is reading and editing files: the PRD, your task board, the design doc, and the code Claude writes. The other is its built-in terminal, which is where Claude Code runs. If you already have VS Code installed, skip to **Turn off Copilot** below.

**Download and install:**

1. Go to [code.visualstudio.com](https://code.visualstudio.com) and click **Download**.
   - **macOS:** Open the downloaded `.zip` file (Safari may unzip it for you) and drag **Visual Studio Code** into your Applications folder.
   - **Windows:** Run the `.exe` installer and accept the defaults. The installer adds VS Code to your PATH.
2. Launch VS Code. You'll see a Welcome page. There's no account to create and nothing to sign in to. If VS Code offers to pick a theme or walk you through the basics, choose what you like or close the tab.

**Turn off Copilot:**

3. VS Code ships with GitHub Copilot, its own AI assistant, and will offer to set it up. You don't need it, and two AI assistants in one window make it hard to tell which one did what. Open the Command Palette (`Cmd+Shift+P` on macOS, `Ctrl+Shift+P` on Windows), type **Preferences: Open User Settings**, and press **Enter/Return**. In the settings search box, type **disable AI features** and check the box for **Chat: Disable AI Features**. The chat panel and the Copilot icons disappear. Claude Code isn't affected: it runs in the terminal, not through VS Code's AI features.

> **Already use Copilot?** Do step 3 anyway while you work through this tutorial, so you always know which assistant you're talking to. Uncheck the same box later to get Copilot back.

> **Optional: the Claude Code extension.** Anthropic also publishes a Claude Code extension for VS Code, with a chat panel and a diff view. This tutorial doesn't use it. Everything happens in the terminal, where every Claude Code command works, and one place to look keeps things simple. If you're curious, try it after you finish Part 2 and see which you prefer.

> **Checkpoint:** VS Code opens to its Welcome page, and the Copilot chat icon is gone from the top and bottom of the window.

---

### 2.2 Git

> **What is Git?** Git is **version control** software; it tracks every change to your files over time. Instead of ending up with `report_v2_final_REAL.xlsx`, Git maintains a clean history of what changed, when, who changed it, and why. It's standard in software development and data engineering. Every company you'll work at uses Git or something built on top of it.

```
Without Git:                    With Git:

essay.docx                      essay.docx
essay_v2.docx                   (Git tracks all versions internally)
essay_final.docx
essay_REAL_final.docx           git log shows:
essay_final_v2_FINAL.docx        v1 --> v2 --> v3 --> current
```

With Git, you have one file. The entire history lives inside a hidden `.git` folder. You can go back to any previous version at any time. This becomes essential when multiple people work on the same codebase, which is the norm in professional settings.

**Check if Git is already installed:**

Open the terminal in VS Code (Terminal --> New Terminal) and run:

```bash
git --version
```

If you see a version number (for example, `git version 2.39.0`), Git is already installed. Skip ahead to **Configure Git** below.

**macOS install:**

1. If Git isn't installed, typing `git --version` in the terminal triggers a prompt to install **Command Line Tools for Xcode**. Click **Install** and wait for it to finish (this may take several minutes).
2. Once installation completes, run `git --version` again to confirm.

**Windows install:**

1. Download the installer from [git-scm.com/download/win](https://git-scm.com/download/win) (64-bit recommended).
2. Run the installer. Most defaults are fine, but pay attention to these settings:
   - Select **"Git from the command line and also from 3rd-party software"** (the recommended option) so Git works in VS Code's terminal. Don't pick "Use Git from Git Bash only," which would hide Git from VS Code. This option also installs **Git Bash**, which the Superpowers plugin (Section 2.5) needs to load on Windows.
   - Select **"Use the OpenSSL library"**
   - Select **"Checkout Windows-style, commit Unix-style line endings"** to prevent line ending issues when collaborating with macOS users.
   - Accept other defaults.
3. After installation, **restart VS Code** completely (close and reopen it).

**Configure Git (both platforms):**

Run these two commands in the terminal, replacing the placeholder values with your actual name and email:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

> **Why use your GitHub email?** When you make commits, Git stamps them with the name and email you configure here. If you use the same email as your GitHub account, GitHub can link your commits to your profile. This means your contributions show up on your GitHub activity graph and your profile page, visible to recruiters and collaborators. Use a mismatched email and your commits will appear as if they came from a stranger.

> **Checkpoint:** `git --version` shows a version number (2.x.x or higher). `git config --list` shows your name and email.

---

### 2.3 Python 3.11+

> **Why Python?** Python is the dominant language in data science, analytics, and AI. Pandas, scikit-learn, TensorFlow, Streamlit: the tools you use in your coursework and will use in your career are all Python-based. You need Python 3.11 or higher installed so you can run the dashboard application you'll build in Part 2.

**Check your current version:**

```bash
python --version
```

or (on macOS, which often requires the `python3` command):

```bash
python3 --version
```

If you see Python 3.11 or higher (for example, `Python 3.12.5`), skip to the next section.

**macOS install:**

1. Go to [python.org/downloads](https://www.python.org/downloads/) and download the latest Python 3 installer (the big button at the top of the page).
2. Open the `.pkg` file and follow the installation wizard.
3. On the final screen, click **Install Certificates** if that option appears. This installs SSL certificates Python needs to make secure web requests.
4. Open a **new terminal** (Terminal --> New Terminal).
5. Verify: `python3 --version`

**Windows install:**

1. Go to [python.org/downloads](https://www.python.org/downloads/) and download the latest Python 3 installer (the big button at the top of the page). You may also see a "Python install manager" option; ignore it and use the standard installer.
2. Run the installer. **Critical: Check the box "Add Python to PATH"** at the bottom of the first screen. If you miss this step, Windows won't know where to find Python when you type `python` in the terminal.
3. Click **Install Now** and complete installation.
4. Open a **new terminal** (Terminal --> New Terminal).
5. Verify: `python --version`

> **macOS note: `python` vs. `python3`.** On current versions of macOS, the plain `python` command usually doesn't exist at all ("command not found"). The installer from python.org installs the new version as `python3`. On macOS, always use `python3` unless you've specifically configured otherwise.

> **Checkpoint:** `python3 --version` (macOS) or `python --version` (Windows) shows Python 3.11 or higher.

---

### 2.4 Claude Code

> **What is Claude Code?** Unlike the Claude web interface at claude.ai where you chat in a browser, Claude Code runs *directly in your terminal*, inside your project. It can read your files, write code, run commands, execute tests, and even update your project's task list as it works. It's an AI agent that can see your entire project and make changes alongside you. This is different from copying code out of a chat window; Claude Code works inside your development environment.

**Step 1: Install Claude Code**

Claude Code has a native installer that handles everything automatically, including background updates.

**macOS:**

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows (PowerShell):**

```powershell
irm https://claude.ai/install.ps1 | iex
```

**Step 2: Read the installer's setup notes**

The installer ends with **Claude Code successfully installed!** and, under that, a **Setup notes** section. Read those notes before you do anything else. Look for one that says `~/.local/bin` (macOS) or your `.local\bin` folder (Windows) **is not in your PATH**. That means Claude Code is on your computer but your terminal doesn't know where to look for it. Opening a new terminal won't fix that on its own, and typing `claude` will get you "command not found" until you follow the note. If there are no setup notes, skip to Step 3.

**macOS:** The note gives you one command to run. Copy it from your own terminal, since it names your shell's startup file (usually `~/.zshrc`). It looks like this:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
```

The first half adds a line to your shell's startup file so every future terminal knows about `~/.local/bin`. The second half loads it into the terminal you're in now. Open a new terminal (Terminal --> New Terminal) and run `claude --version` to confirm.

**Windows:** The note names the folder (usually `C:\Users\YourName\.local\bin`) and tells you to add it yourself:

1. Copy the folder path from the note.
2. Press the Windows key, type **environment variables**, and open **Edit environment variables for your account**.
3. Under **User variables**, select **Path** and click **Edit**.
4. Click **New**, paste the folder path, and click **OK** on each window to close them.
5. Close VS Code completely and reopen it. A new terminal tab inside VS Code isn't enough on Windows: VS Code reads the PATH once when it starts, so it has to restart to see the change.

Then open a terminal and run `claude --version` to confirm.

**Step 3: Authenticate**

1. In the terminal, type `claude` and press Enter.
2. The first run asks you to pick a text style. Press Enter to keep the default, then press Enter again on **Claude account with subscription**.
3. A browser window opens. Log in with your Claude account (the one with the Pro subscription from Section 1.2) and authorize Claude Code to access your account.
4. Return to the terminal. Press Enter through the "Login successful" and "Security notes" screens and the terminal-setup question (either answer is fine). You should see Claude Code's interactive prompt.
5. Type `/exit` to quit for now. You'll come back to Claude Code in Section 2.5 and use it throughout Part 2.

> **If authentication fails:** Run `claude auth logout` in the terminal (or type `/logout` inside Claude Code), then run `claude` again. Make sure your browser allows popup windows. The authentication flow opens a new browser tab. If you're using a browser with aggressive popup blocking, temporarily allow popups for the authentication URL.

> **Checkpoint:** `claude --version` prints a version number, and running `claude` starts an interactive session. Type `/exit` to quit.

---

### 2.5 Superpowers plugin

> **What is Superpowers?** [Superpowers](https://github.com/obra/superpowers) is a Claude Code plugin that gives Claude a library of skills. A skill is a small piece of expertise Claude pulls in when your prompt matches it. Three skills you'll use in Part 2: `brainstorming` (asks clarifying questions and produces a design document), `writing-plans` (turns a design into a bite-sized implementation plan), and `executing-plans` (works through the plan task by task with frequent commits). The skills auto-invoke based on what you ask Claude to do, so you don't have to memorize commands.

#### Skills primer

Skills are markdown files that ship with the Superpowers plugin. Each one teaches Claude how to handle a specific type of task. When you ask Claude to design something, the brainstorming skill activates. When you ask Claude to implement a plan, the executing-plans skill activates. Claude reads each skill's description at session start and matches your prompt against those descriptions to decide which skill to load. Each skill it loads shows up in the output as a `Skill(superpowers:<name>)` line, like `Skill(superpowers:brainstorming)`. That visibility is the whole reason this works as a teaching tool.

Here's the flow you'll see in Part 2: you never call a skill by name; your plain-English prompt triggers the chain:

```
You type a plain-English prompt
("Help me design and plan the dashboard")
              |
              v
     using-superpowers          <- loaded at session start;
     reads your intent             matches your words to a skill
              |
              v
  brainstorming ──► writing-plans ──► executing-plans
  (clarifies and     (turns it into     (builds it task by
   writes a          a step-by-step      task, testing and
   design doc)       plan)               committing)
              |
              v
  Each step shows up as: Skill(superpowers:<name>)
  (that line is your cue a skill kicked in)
```

This tutorial was written against Superpowers 6.3.0. The plugin updates itself, so a skill's wording may drift a little from what Part 2 quotes, but the steps stay the same.

The install command below is the only time you'll type a slash command to use Superpowers. The skills themselves never need one; they activate from natural-language prompts. (You'll still type a few unrelated slash commands elsewhere in the tutorial, like `/exit` and `/init`.)

#### Install the plugin

1. Open your terminal in VS Code (Terminal --> New Terminal) and run `claude` from any directory:

   ```bash
   claude
   ```

   The first time you start Claude Code in a folder, it asks whether you trust the folder. The highlighted answer is **No, exit**, so press the down arrow to **Yes, I trust this folder** and press Enter.

2. Inside Claude Code, run:

   ```
   /plugin install superpowers@claude-plugins-official
   ```

3. Claude Code shows the plugin's details and asks where to install it. Press Enter on **Install for you (user scope)**. The install takes about 30 seconds, and Claude Code confirms the plugin is active. If it tells you to run `/reload-plugins` instead, run that. From now on Superpowers loads at the start of every session.

4. Confirm it's installed. Ask Claude: `Is the Superpowers plugin installed?` Claude will check and confirm. (There's no startup banner to look for; Superpowers shows itself later, whenever a skill activates and shows up as a `Skill(superpowers:<name>)` line. You can also run `/plugin` to see your installed plugins.)

> **Windows:** Superpowers loads through Git Bash, which the Git installer set up in Section 2.2 when you chose the recommended option. If the plugin installs but Claude says it isn't active in a new session, check that Git Bash exists (search for it in the Start menu). If it's missing, rerun the Git installer with the recommended options.

> **Checkpoint:** In a Claude Code session, asking `Is the Superpowers plugin installed?` gets a yes.

---

## Section 3: Create your repository and clone it (~15 min)

### Understanding templates and clones

Before you do anything, it helps to understand the two-step process you're about to follow and why it works this way.

```
+------------------+  Use this    +------------------+
|  Tutorial repo   |  template    |   Your repo      |
|  (LMU-ISBA)      |  ---------->  |   (GitHub)       |
+------------------+              +--------+---------+
                                           | Clone
                                           v
                                  +------------------+
                                  |  Your Computer   |
                                  |  (Local Copy)    |
                                  +------------------+
```

- **Template** = the tutorial repo is marked as a template on GitHub, so you can stamp out a brand-new repository of your own from it: the same files, a clean history, your name on it. Changes you make to your repo don't affect the tutorial, and nothing links back.
- **Clone** = downloading your repo from GitHub to your computer so you can work on files locally. This is where you actually edit code.

The flow is: you edit files on your computer (local), then **push** changes up to your repo on GitHub. Your repo is your own space. You can't accidentally break the tutorial.

> **Why a template and not a fork?** GitHub also offers **Fork**, which makes a linked copy that keeps pointing back at the original. That's the right tool when you plan to send changes back to someone else's project. Here you don't. The dashboard is your project, and a linked copy would show "forked from LMU-ISBA" on your profile and try to send any pull request you open to the tutorial repo instead of your own. A template gives you a repo that reads as your work, with a commit history that starts with you.

---

### 3.1 Create your repository

1. Go to [github.com/LMU-ISBA/ai-dev-workflow-tutorial](https://github.com/LMU-ISBA/ai-dev-workflow-tutorial).
2. Click the green **Use this template** button in the upper-right corner of the page, then **Create a new repository**.
3. On the "Create a new repository" page:
   - **Owner:** your GitHub account.
   - **Repository name:** `ai-dev-workflow-tutorial`. Keep this name; Part 2's instructions use it.
   - Leave **Include all branches** unchecked.
   - Choose **Public**. Streamlit Community Cloud deploys public repos for free, and this is portfolio work.
4. Click **Create repository** and wait for GitHub to finish.

> **Checkpoint:** The repository is visible at `github.com/[your-username]/ai-dev-workflow-tutorial`, with the tutorial's files and one commit, "Initial commit," from you. (GitHub adds a small "generated from LMU-ISBA/ai-dev-workflow-tutorial" note under the name. That's a label, not a link: the repo is fully yours.)

---

### 3.2 Clone your repository

Cloning downloads the repository to your computer so you can work on it locally.

1. On your new repository page (`github.com/[your-username]/ai-dev-workflow-tutorial`), click the green **Code** button.
2. Make sure the **HTTPS** tab is selected (not SSH or GitHub CLI).
3. Copy the URL. It will look like: `https://github.com/[your-username]/ai-dev-workflow-tutorial.git`
4. In VS Code, open the Command Palette (`Cmd+Shift+P` on macOS, `Ctrl+Shift+P` on Windows), type **Git: Clone**, and press **Enter/Return**. (The Welcome page's **Clone Git Repository** link does the same thing.)
5. Paste the URL you copied and press **Enter/Return**.
6. Choose a save location. **Recommended:** Create a `GitHub` folder in your home directory to keep all repositories organized:
   - macOS: `~/GitHub`
   - Windows: `C:\Users\YourName\GitHub`
7. When VS Code asks whether to open the cloned repository, click **Open**. If it then asks whether you trust the authors of the files in this folder, click **Yes, I trust the authors**. That unlocks the terminal and the other features you'll need in this folder.

A full copy of your repository now lives on your computer, in the folder you chose. These local files are yours to edit; your changes stay on your machine until you push them back to GitHub (you'll do that in Part 2).

> **Back up your work:** Once you push to GitHub (Part 2), your committed code is safe in the cloud. To protect everything else, including changes you haven't committed yet, put your `GitHub` folder somewhere your computer already syncs to cloud storage. Common options: iCloud Drive (macOS), OneDrive (Windows), Google Drive, or Dropbox. Then if your laptop is lost, stolen, or dies, your work is waiting for you on the next machine.

> **Organizing your repositories:** Keeping all your Git repositories in a single `GitHub` folder (rather than scattering them across Desktop, Documents, and Downloads) is a small habit that pays off as you accumulate projects. It makes finding projects easy and keeps your file system clean.

> **If you can't see the Explorer sidebar in VS Code:** Press `Cmd+B` (macOS) or `Ctrl+B` (Windows) to toggle the sidebar. The Explorer shows your project's file and folder structure.

> **Checkpoint:** Tutorial files are visible in VS Code's Explorer (left sidebar). You should see the `data/` and `prd/` folders, along with `README.md`, `pre-work-setup.md`, and `workshop-build-deploy.md`.

---

## Section 4: Final verification (~10 min)

Before calling Part 1 complete, run through every item in this checklist. Each verification step confirms that a tool is correctly installed and accessible.

### Accounts

- [ ] Can log into [github.com](https://github.com) and see your dashboard
- [ ] Claude Pro subscription active at [claude.ai](https://claude.ai) (Pro badge visible)

### Tools

Open a terminal in VS Code (Terminal --> New Terminal) and run each command:

```bash
git --version
```
Expected output: `git version 2.x.x` (any 2.x version is fine)

```bash
python3 --version       # macOS
python --version         # Windows
```
Expected output: `Python 3.11.x` or higher (3.12.x, 3.13.x are all fine)

```bash
claude --version
```
Expected output: a version number

### Superpowers plugin

Start a Claude Code session:
```bash
claude
```
Then ask Claude: `Is the Superpowers plugin installed?` Expected: Claude checks and confirms it's installed (it can run `/plugin` to verify). Type `/exit` to close the session.

If any command fails with "command not found," open a new terminal and try again. If `claude` is the one that fails, go back to Section 2.4, Step 2, and check the installer's setup notes: the PATH fix there is the usual cause. If it still fails, read the error, ask Claude Code to help, or reach out on Teams (the General channel, or a direct message to me).

### Repository

- [ ] Your own repository created from the template (`github.com/[your-username]/ai-dev-workflow-tutorial`)
- [ ] Repo cloned locally and open in VS Code
- [ ] Files visible in VS Code's Explorer (you should see `data/`, `prd/`, and the `README.md`, `pre-work-setup.md`, and `workshop-build-deploy.md` files)

---

### Understanding what you've built

Here's what you've just configured:

```
+---------------------------------------------------------------+
|                  Your Environment (Complete)                    |
+---------------------------------------------------------------+
|                                                                |
|  Cloud Services:                                               |
|    GitHub ............. Code hosting and collaboration          |
|    Claude Pro ......... AI assistant subscription               |
|                                                                |
|  Local Tools:                                                  |
|    VS Code ............ Code editor and terminal                |
|    Git ................ Version control                         |
|    Python 3.11+ ....... Programming language                   |
|    Claude Code ........ AI coding agent                         |
|    Superpowers ........ Skill-driven planning (Claude plugin)   |
|                                                                |
|  Your Repository:                                              |
|    Repo on GitHub ..... Your remote copy                       |
|    Clone on computer .. Your local working copy                |
|                                                                |
+---------------------------------------------------------------+
```

These tools connect into one workflow: GitHub hosts your code, Git tracks changes, VS Code is where you read and edit it, the Superpowers plugin's skills help Claude plan, and Claude Code builds alongside you. In Part 2, you'll add a `TASKS.md` file to track your work, then see everything work together as you plan, build, and deploy a live dashboard.

> **Before you start Part 2:** If anything above isn't working, reach out on Teams now, either in the General channel or with a direct message to me. It's much easier to sort out setup problems before you start building than in the middle of it.

---

## What's next

Part 1 is complete. You've:

- Created accounts on GitHub and Claude
- Installed the tools that make up your development environment: VS Code, Git, Python, Claude Code, and the Superpowers plugin
- Created your own repository from the tutorial template and cloned it (your working copy of the project)

Every tool you just set up transfers directly to your capstone project: Git and GitHub for team collaboration, and Claude Code with the Superpowers plugin for turning requirements into bite-sized plans. Two more tools for the capstone itself, Granola for meeting notes and Wispr Flow for dictation, are in the [capstone tools appendix](capstone-tools.md). Skip them for now.

**With setup done, you're ready for Part 2.** In the build guide, you'll put everything together:

1. **Set up your `TASKS.md` board** so you (and Claude Code) can track every task from *To Do* to *Done*, all inside your repository.
2. **Plan with Superpowers** by letting the brainstorming skill produce a design document, then having writing-plans turn it into a bite-sized implementation plan.
3. **Build a Streamlit dashboard** with Claude Code's help, working from the structured plan.
4. **Commit, push, and deploy** your dashboard so it's live and shareable on the internet.

The tools are ready. Next, you build.

Continue to [**Part 2: Build & Deploy**](workshop-build-deploy.md).
