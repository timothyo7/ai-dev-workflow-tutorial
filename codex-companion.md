# Using Codex instead of Claude Code

**For students who already pay for ChatGPT. Read this beside the tutorial, not instead of it.**

The tutorial is written for Claude Code. If you have a ChatGPT subscription, it includes Codex, OpenAI's coding agent, which does the same job, and there's no reason to pay for two. The workflow you're learning doesn't change. The Superpowers plugin runs on Codex, so brainstorming, writing-plans, and executing-plans work the same way. Every plain-English prompt in Part 2 is the same, and so are the files you produce: the board, the spec, the plan, and the commits. What differs is the plumbing: how you install and sign in, how you install the plugin, what the permission modes are called, and a handful of commands. This page lists every one of those points, in tutorial order. Where a section isn't listed, follow the tutorial as written.

Verified on 2026-09-02 against the Codex docs at https://learn.chatgpt.com/docs (CLI 0.153.0) and a local install of CLI 0.144.5. Codex changes as often as Claude Code does. If a menu or command here doesn't match what you see, work out the equivalent (the "heads up" advice in Part 1 applies), then tell me what changed. You're on the less-documented road, and your notes improve this page for the next person.

> **Two offers worth claiming before you start.** OpenAI's 2026 back-to-school offer gives verified US college students four months of ChatGPT Plus free. Claim it by October 31, 2026 at https://chatgpt.com/students/2026. There's also $100 in Codex usage credits for verified US and Canada students at https://chatgpt.com/codex/offers/students. A free ChatGPT account can run Codex, but its limits are small. Plus is the plan this page assumes.

---

## Part 1: Setup

### 1.2 Claude Pro subscription

Skip it. You'll sign in to Codex with the ChatGPT account you already have.

What Plus gives you in Codex: the GPT-5.6 models (Sol is the default and is plenty for this tutorial), a 5-hour usage window, and weekly limits. Inside Codex, `/status` shows your model and usage, and `/usage` shows how much of each window is left. Plus can also buy extra credits. Nothing in this tutorial needs them.

### 2.1 VS Code

Same as the tutorial, including turning off Copilot. OpenAI publishes a Codex extension for VS Code (search the Extensions view for **Codex – OpenAI's coding agent**, publisher OpenAI). Like the Claude Code extension, it's optional here: this tutorial runs the agent in VS Code's terminal, where every command works and there's one place to look. The extension bundles its own copy of Codex, so you still need the command-line install below to type `codex` in the terminal.

### 2.4 Claude Code

Install the Codex CLI instead.

**macOS:**

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"
```

Codex runs natively in PowerShell on Windows 11, with its own sandbox. You don't need WSL, and you don't need Git Bash for the plugin (that requirement is Claude Code's).

After installation, open a **new terminal** (Terminal --> New Terminal) so the PATH updates take effect.

**Sign in:**

1. In the terminal, type `codex` and press Enter.
2. Choose **Sign in with ChatGPT**. A browser window opens. Sign in with your ChatGPT account and return to the terminal.
3. Type `/quit` to leave for now.

> **If sign-in fails:** run `codex logout`, then `codex` again. `codex login status` tells you whether you're signed in, and `codex doctor` checks the install.

> **Checkpoint:** `codex --version` prints a version number, and `codex login status` says you're signed in.

### 2.5 Superpowers plugin

The plugin comes from OpenAI's own plugin marketplace, and skills fire automatically in Codex without any hook, so this is shorter than the Claude Code version.

1. Run `codex` from any directory.
2. Type `/plugins`, search for **superpowers**, and choose **Install Plugin**.
3. Skills become available in a new session, so type `/new` (or quit and start `codex` again).
4. Confirm it's installed. Ask Codex: `Is the Superpowers plugin installed?` You can also type `/skills` and look for `brainstorming`, `writing-plans`, and `executing-plans` in the list.

Subagents, which Superpowers uses for its recommended execution mode, are on by default in current Codex releases. There's nothing to configure.

Read the tutorial's skills primer as written. One difference: Claude Code prints a `Skill(superpowers:brainstorming)` line when a skill loads, and Codex doesn't announce skills the same way. If you're ever unsure which skill is driving, ask: `Which skill are you using right now?` You can also call a skill on purpose by typing `$` and picking it from the list. This tutorial never needs that.

> **Checkpoint:** In a Codex session, asking `Is the Superpowers plugin installed?` gets a yes.

### Section 4: Final verification

Under **Tools**, run `codex --version` instead of `claude --version`. Under **Superpowers plugin**, start `codex` instead of `claude`. Everything else is the same.

---

## Part 2: Build and deploy

### Prerequisites check

`codex --version` in place of `claude --version`.

### Section 1, step 1: Start Claude Code

Run `codex` instead of `claude`. The first time you open Codex in a folder it may ask whether you trust the files there. Say yes. It's your repository.

### Section 1, step 2: Set the output style to Explanatory

Codex has no output styles, and its `/personality` setting changes tone, not how much it explains. You get the same effect with a short instructions file that Codex reads at the start of every session, in every project. In Codex, send:

```
Create a file at ~/.codex/AGENTS.md with this content, exactly:

# How to work with me
I'm learning. Before you change anything, say in a sentence or two what
you're about to do and why. After each change, explain what you did in
plain language and point out anything I should read or decide. Keep code
simple and readable.
```

Codex will ask permission to write outside the project folder. Approve it. Then type `/new` so the session picks the file up. Skip the `/clear` step in the tutorial. `/new` did the same thing.

The **Learning** style has no Codex equivalent. If you want to write parts of the code yourself, add a line to the file: "Leave the small, clearly marked pieces of each function for me to write."

### Section 1, step 4: The `@` symbol

Works the same. Type `@` and pick the file.

### Section 2.1: Optional status line

`/statusline` exists in Codex too, and the same request works.

### Section 2.2: Brainstorm and plan

Identical, including the ground rules, the visual companion (say no), the spec review, and the choice of inline execution. The only difference is the missing `Skill(...)` line noted above.

### Section 4: Claude Code permission modes

Codex's modes have different names and no Shift+Tab. Type `/permissions` to see them:

| Codex mode | What it does | The tutorial's equivalent |
|---|---|---|
| **Ask for approval** (the default) | Edits files inside your project and runs routine commands on its own. Asks before anything that reaches outside the project or the internet | Manual, roughly. Codex asks less often than Claude's Manual, because it lets ordinary in-project commands through |
| **Approve for me** | A second reviewer agent looks at each request and approves the routine ones for you | Auto |
| **Read only** | Reads and proposes. Changes nothing | Plan |
| **Full access** | Everything runs with no sandbox and no questions. Not for this tutorial | Nothing. Leave it alone |

Follow the tutorial's recommendation with Codex's names: **Ask for approval** for TASK-1, then **Approve for me** from TASK-2 on.

One box you'll see that Claude Code students won't. Codex runs commands in a sandbox with the internet turned off. The first time a step needs the network, such as installing packages into `venv/` or running `git push`, a box appears: **"Would you like to run the following command?"** Read the command, then choose **Yes, just this once**. If it's `git push` and you're tired of the box, **Yes, and don't ask again for commands that start with `git push`** is fine too. The same box can appear when Codex starts the Streamlit server. Approve it.

### Section 4.4: Capture project memory with /init

`/init` in Codex creates **`AGENTS.md`** instead of `CLAUDE.md`. Same idea, same place, different name, and Codex reads it at the start of every session. Everywhere the tutorial says `CLAUDE.md` from here on (the Lessons section, the commit, Sections 6 and 7), read `AGENTS.md`. The commit message becomes "Add project memory (AGENTS.md)".

Codex won't read a `CLAUDE.md` if one turns up in a repo. If a teammate's project has one, `/import` converts it.

Skip the auto memory callout. Codex has a memory feature, but it's off by default, and `AGENTS.md` is your carryover.

### Section 4.5, step 2: Review the branch

Type `/review`, choose **Review against a base branch**, and enter `main`. Codex reads every change on your branch and returns a ranked list of findings without touching your files. From there, the tutorial applies: decide what to fix, tell Codex, and commit the fixes.

### Section 4.5, step 3: Merge into main

Same prompt. Codex will ask permission for the push in step 4. Approve it.

### Section 5: Deploy

Identical. Streamlit Cloud never sees which agent wrote the code.

### Troubleshooting

The tutorial's advice holds: paste the exact error and ask. A few Codex-specific handles:

- `/new` starts a fresh conversation, and `/compact` shortens a long one.
- Press **Esc** twice to step back to an earlier message and continue from there.
- `/status` shows your model and how much of your usage window is left. `/model` switches models if you hit a limit.
- `/quit` leaves. `codex doctor` checks the install if the command itself misbehaves.
- Typing `/` shows the full list of commands. There's no `/help`.

---

## Quick reference

| In the tutorial | In Codex |
|---|---|
| `claude` | `codex` |
| `/exit` | `/quit` |
| `/clear` | `/new` |
| `/config` --> Output style | the `~/.codex/AGENTS.md` file above |
| Shift+Tab (Manual, Accept edits, Plan, Auto) | `/permissions` (Ask for approval, Read only, Approve for me) |
| `/plugin install superpowers@claude-plugins-official` | `/plugins`, search **superpowers**, Install Plugin |
| `Skill(superpowers:brainstorming)` line | none; ask "which skill are you using?" |
| `/init` writes `CLAUDE.md` | `/init` writes `AGENTS.md` |
| `/code-review feature/sales-dashboard` | `/review`, Review against a base branch, `main` |
| `/usage` | `/status` or `/usage` |
| `/rewind` | Esc twice |
| `/statusline` | `/statusline` |
| `claude --version` | `codex --version` |
| `claude auth logout` | `codex logout` |
