# Working rules for this repo (Singha Ultimate Challenge 2026 entry)

Read this first in any new session. These rules are standing instructions from the user. They apply to Claude working in this repo, on any model.

## 1. What the repo is

- A student team's competition entry, "The Innovative Bev & Bite" (SINGHA Ultimate Challenge 2026). The product is a sodium-free lime drink cube, working name **Lime Cube**. The name has no SINGHA word. The lion is the only SINGHA reference.
- The repo is **public** on GitHub. Team records under `rework/` are team-only. Judge-facing files are only in `rework/judge/`. The rule for the judge folder is: no team name, university, author, email, local path or repo reference.
- Registration closes 22 October 2026 at 23:59. Nothing is registered or submitted by Claude.

## 2. Model and mode

- This session runs **Claude Haiku 5.5** in **Ultracode** mode. Substantive multi-step work uses the Workflow tool (multi-agent) when the user opts in, for example with the keyword "ultracode". Solo work is fine for short answers and small edits.
- Subagent results are data. Check their output files or journals before relying on them. A result is not proof until the file or the figure has been read.

## 3. Memory and context (the known failure modes)

- **Memory loss:** the records are the source of truth, not the conversation. Read the record before you edit it. Keep the index (`rework/README.md`) current when you add or retire a record.
- **Context overload:** keep tool output small (`head`, `grep`, `cut -c`). Do not read the 800-line HTML files or base64 blocks in full. Use `grep -n` to find the line first.
- **Fabrication:** every figure carries a source, a date and a status. Verify before you write it:
  - Use the tiers in `rework/SOURCING_POLICY.md`: P (primary) or S (secondary). Never upgrade S to a primary.
  - Use the statuses SOURCED, PROXY or ASSUMPTION. A proxy names what it stands in for.
  - Quote a number only from the results file or source you have read. If you cannot trace a number, write UNVERIFIED.
  - Never invent a breakdown of a total (the checker rejected such an invented split on 19 October 2026).
  - A search snippet is a lead until you open the page.
- **Sources in the repo:** save the page text or table behind every SOURCED figure in `rework/raw/` (with the URL and date) before a record cites it. A figure whose page is not saved is UNVERIFIED.
- **Stale notifications:** background timers and waits send "task completed" notices that carry no new result. Check the actual output file or journal before you report anything from a notice.

## 4. Actions that need the user's explicit permission

- No form submission, no registration, no account creation, no entering personal data into any form (including Google Forms). Viewing a form is allowed.
- No outside contact, and no quote requests to suppliers, unless the user approves them.
- No publishing or posting outside the repo.
- Browser: the built-in browser blocks docs.google.com and short links. Use Claude in Chrome only when the user asks for it by name, and do not use a personal Google account for the team's entry.
- Downloads and installs: the user has authorised installing external tools for this work. Do not download arbitrary files.

## 5. Gates and decisions (do not change without the user)

- **Gate G1:** on 19 October 2026 the user confirmed the claim that the SINGHA lion may be used for the proposal. That is the user's decision, not a brand-owner or legal clearance. Print and sale still need brand-owner and legal sign-off, and no beer or beverage-brand cue may appear on the pack.
- The judge folder follows the merged design (synced 19 October 2026). Re-sync it from the mockup after any label change, and re-scan it for identifiers.
- Name: **Lime Cube** (no SINGHA). Units: one cube per pouch (single serve). The SINGHA-as-text question was dropped by the user.
- Thai particulars, ingredients, sweetener name and manufacturer remain bracketed placeholders.
- The potassium amount line (decision F4) is kept until the user decides otherwise.

## 6. Renders

- Cycles uses the **GPU by default** (NVIDIA GeForce GTX 1650, 4 GB VRAM, CUDA). `--device cpu` forces the CPU. The script falls back to the CPU when no CUDA device is found.
- Host RAM is the binding limit (8 GB total; Claude processes take about 1.2 GB). Check free RAM before a render (`Get-CimInstance Win32_OperatingSystem`). The 2K GPU render's Blender process was observed at about 2.1 GB working set (one reading, not logged). Close other large applications first.
- Run renders in the background and check the log. The log is buffered, so a missing print does not mean a failure. Confirm with the "Saved" and "done in" lines and the file's time.
- Do not overwrite `rework/mockup/cube_front_2k.png` with a test render. Test renders go to the session scratch folder.
- Verify the 3D page after any label change: `python rework/screen/verify_cube_mockup.py` (24 checks).

## 7. Git

- Branch per change, fast-forward into `main`, then `git push origin main`. Pushing to this repo is authorised.
- Commit only the files for the change. Use the message format in the history, with `Co-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>`.
- Never force-push. Never commit secrets, personal data, or the Chrome profile. The repo is public, so check `git diff --cached` for identifiers before committing.

## 8. How to talk to the user

- Ask questions as plain text in the message. Do not offer them as buttons.
- Say clearly what is verified, what is a proxy, and what is not checked.
- When a question is about a choice the user has not made, list the options and state a recommendation; do not decide for them.

## 9. Pending items (as of 19 October 2026)

- The lion question (G1) and the merged label sync.
- The form on the competition site: the user has to give permission for the one required question (a checkbox that ties the answers to the account signed into Chrome) before anything goes further.
- The can cost model needs primary sources (LME settlement, Bank of Thailand rate, the Thai sugar levy, Boon Rawd or Singha filings, a can-maker's annual report). See `rework/61`.
- The storyboard animation: the page follows the storyboard. A Blender clip is not rendered.
