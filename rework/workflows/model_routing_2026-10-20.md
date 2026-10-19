# Model routing for the deck diligence workflow (20 October 2026)

Set by the user on 20 October 2026. The script is `.claude/workflows/singha-deck-diligence-loop.js`.

## Routing

| Stage | Tasks | Model | Why |
|---|---|---|---|
| Author (research, models, drafting) | All 16 | Haiku 5.5 | Cheap search and drafting; the verifier is the check |
| Verify and revise, routine | T1 to T7, T13, T16, T68 | Haiku 5.5 | Source checking and text, no hard statistics |
| Verify and revise, hard | T8, T9, T10, T11, T12, T14, T15 | Sonnet (or higher) | Chemistry, stoichiometry, medical-regulatory reading, value and Monte Carlo statistics |
| Critic (coverage check) | Once | Haiku 5.5 | Reads summaries only |

Opus is reserved for a single final check of T14 (the significance conclusion), and only when the weekly meter has clear headroom. It is not part of the default run.

## Usage limit (Claude Max plan, x20)

Snapshot read by the user on 20 October 2026 at about 02:07 (phone clock):

- Current session: 32% used, resets in about 1 hour 13 minutes.
- Weekly, all models: 80% used, resets in about 10 hours 53 minutes.
- Weekly, Fable only: 0% used.
- Usage credits: off, balance 7.41 credits. When a limit is reached the run stops; it does not buy more usage.

Rules that follow from this:

1. Check the weekly meter before any Sonnet or Opus pass. The workflow cannot read the meter.
2. Proposed thresholds, for the user to confirm: launch the hard-task Sonnet pass only when the weekly meter is at 60% or below, or after the weekly reset. Launch Opus only when it is at 50% or below.
3. Run the hard-task pass with `args.only` set to the hard tasks, so routine tasks are not repeated.
4. Keep `args.maxRounds` at 2 unless the user asks for more. Each extra round adds a Sonnet verify and a Sonnet revise per hard task.

## How the pass is resumed without repeating work

- A completed agent call is cached when its prompt and options are unchanged. The author calls stay on Haiku, so they are reused.
- Only the hard-task verify and revise calls change model, so only they run again.
- The prior run must be stopped before a resume. The Haiku run `wf_cb1b4bf7-df3` (task `wrv2tt5je`) is still active; stop it, then resume with `resumeFromRunId` once it has finished or is stopped.

## Records affected

- `rework/workflows/deck_diligence_prompt_2026-10-20.md` lists the tasks; this note adds the model for each.
- Stage-1 output from the stopped Sonnet run is archived in `rework/archive/diligence_sonnet_partial_2026-10-20/` (unverified, not for citation).
