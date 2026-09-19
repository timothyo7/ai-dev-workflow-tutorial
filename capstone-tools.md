# Appendix: Capstone tools

**Granola and Wispr Flow. Not needed for the tutorial; set them up when your capstone starts.**

Two tools pay off once you're working with real stakeholders. [Granola](https://www.granola.ai) is an AI notepad that records your meetings. Once it's connected, Claude Code can read your notes, so "what did the client ask for in Tuesday's meeting?" gets answered from the record rather than your memory. [Wispr Flow](https://wisprflow.ai) is dictation, so you can give Claude a few paragraphs of context by voice instead of typing them. Both have student plans. Do this appendix after you've finished the tutorial, so you already have VS Code, Claude Code, and the habits from Part 2.

## A. Granola

### A.1 Granola account and student plan

> **Why Granola?** Granola is an AI notepad for meetings. It listens while you talk, then turns the conversation into clean, searchable notes, so you can pay attention instead of scrambling to type. It pays off in your **capstone**: when you meet with stakeholders, Granola captures what was said, and (in A.2) you connect it to Claude Code so you can pull those meeting notes straight into a build session: "what did the client ask for in Tuesday's meeting?" answered from your actual notes, not your memory.

**Steps:**

1. Go to [granola.ai/students](https://www.granola.ai/students) and click **Apply**. Sign up with your **school email** and follow the prompts to verify you're a current student.
2. The student plan gives you **12 months of Granola Business free**. It's available to enrolled students at accredited universities in the **US, UK, and Canada**.

> **Not eligible for the student plan?** No problem. Granola's free **Basic** plan works too; the only limit is that Claude Code can query your notes from the **last 30 days** rather than your whole history. Sign up at [granola.ai](https://www.granola.ai) without the student application.

> **Checkpoint:** You can sign in to your Granola account (student application submitted or approved).

---

### A.2 Granola app, connected to Claude Code

This is the payoff of the Granola account above. You'll install the app and then give Claude Code the ability to read your meeting notes.

**Install the app:**

1. Download the Granola desktop app from [granola.ai](https://www.granola.ai) and install it.
2. Open Granola and sign in with the account you created in A.1. If you're unsure which email that account uses, check under **Settings** in Granola after signing in; you'll need the same email when you authorize Claude Code below.
3. *(Optional but useful)* Record one short test note (even a few minutes of a lecture or a chat with a classmate) so you have something for Claude Code to find later.

**Connect it to Claude Code:**

4. In **VS Code's terminal** (not inside Claude Code), register Granola as a connection. (MCP is the connector standard Claude Code uses to reach outside services. Your capstone materials cover it; for now the command is enough.) You can run this from any directory, and it only needs to be done once:

   ```bash
   claude mcp add --transport http granola https://mcp.granola.ai/mcp
   ```

5. Start Claude Code:

   ```bash
   claude
   ```

6. Inside Claude Code, open the MCP menu:

   ```
   /mcp
   ```

   You'll see `granola` listed, likely showing that authentication is required.

7. Select `granola` with the **arrow keys**, press **Enter**, and choose **Authenticate**. A browser window opens; sign in to Granola with the **same email** as your account, authorize the connection, and return to the terminal.

8. Test it. In Claude Code, ask:

   ```
   Which Granola account am I signed in with?
   ```

   Claude uses Granola's `get_account_info` tool and replies with your email and workspace. This works even if you have no notes yet, which makes it a clean way to confirm the connection. If you recorded a test note in step 3, try: `Summarize my most recent meeting.`

> **If it can't reach your notes:** Run `/mcp`, select `granola`, and re-authenticate. If you see "Unauthorized: user has not created a Granola account yet," you signed in with a different email than your Granola account; check the account email in Granola's **Settings** and reconnect with that one.

> **How you'll use this in your capstone:** After a stakeholder meeting, open a Claude Code session in your capstone repo and ask things like *"From my meeting notes this week, list what the client asked us to change,"* or *"Draft tasks in TASKS.md based on the decisions in yesterday's kickoff."* Your meeting record flows straight into the plan-and-build workflow you're learning here.

> **Checkpoint:** `/mcp` shows `granola` as authenticated, and asking "Which Granola account am I signed in with?" returns your email.

---

## B. Wispr Flow

### B.1 Wispr Flow account and student plan

> **Why Wispr Flow?** Wispr Flow is a voice dictation app that turns your speech into text in any application, including the VS Code terminal where Claude Code runs. It advertises around 4x faster than typing and cleans up filler and false starts as you talk. Here's why it earns a spot in your capstone toolkit: what you get out of an AI agent depends on how much context you put in. In the tutorial's Part 2, the Superpowers `brainstorming` skill interviews you with clarifying questions, and the richer your answers, the better the design and plan it produces. Speaking a few paragraphs of context is far easier than typing them, so dictation is the fastest way to give Claude the detailed direction it works best with.

**Steps:**

1. Go to [wisprflow.ai/students](https://wisprflow.ai/students) and click **Start Today for free** to create your account.
2. Download the app for your platform (macOS or Windows) and install it.
3. Sign in with your **school (.edu) email** to auto-activate the student offer. No .edu address? Use the form on that page to verify with a student ID, enrollment confirmation, or similar.

The student offer is **3 months free**, then $6/month billed annually (50% off the standard price). You can cancel anytime.

> **Checkpoint:** Wispr Flow is installed, and you can dictate a sentence into any text field and watch it appear as text. (Finish the app's onboarding first; it sets the key you hold to talk.)

---

## Verification

- [ ] Can sign in to Granola (student plan applied, or the free Basic plan)
- [ ] Wispr Flow installed and dictating (student offer activated with your school email)

### Granola (Claude Code connection)

Start a Claude Code session, run `/mcp`, and confirm `granola` is listed and authenticated. Then ask:
```
Which Granola account am I signed in with?
```
Expected: Claude returns your Granola email and workspace. Type `/exit` to close the session.

- [ ] `granola` shows as authenticated in `/mcp`
- [ ] "Which Granola account am I signed in with?" returns your email
