# BRIEF_MYTHOS_READ.md — single-case forensic read of the released Mythos 5 transcript

This is a **descriptive, single-case** forensic read of ONE public transcript:
the released Claude Mythos 5 incident transcript (anthropics/mythos-5-incident-transcript on GitHub;
PDF mirror on the Anthropic CDN). It is the PyPI-upload incident with summarized chain-of-thought (CoT)
and multiple context compactions. Goal: document, per compaction boundary, what the summary kept, dropped,
hardened, or distorted — especially for situational beliefs. **No statistics, no causal claims, no reruns.**

## Non-negotiables (same failures we keep hitting)
1. **A transcript log is not the model's context.** After a compaction the model saw only
   [system prompt] + [latest compaction summary] + [turns after the cut]. "After" = the turns reading from
   the summary, NOT merely "later in the file." Reconstruct the actual post-compaction context before judging.
2. **This is summarized CoT, not raw reasoning.** "The hedge is absent" means absent from the summarized
   trace, not proof it wasn't thought. Say so in every finding.
3. **n = 1.** Output is a quoted, structured case description. Never generalize ("compaction causes…");
   at most "in this transcript, the summary stated X as fact where the prior CoT hedged it."
4. **Every claim needs three quoted spans** (pre-CoT, summary, post-CoT) or it is not made.
5. If anything in the file is ambiguous (which block is a compaction, which turn is pre vs post),
   flag it in `UNCERTAIN.md` rather than guessing.

## Step 0 — ingest and scaffold (do this first, then STOP and report)
- Download the transcript (GitHub repo or PDF). If a fetcher truncates it, note that and work from the
  local copy. If Transect (github.com/AI-Safety-Institute/transect) ingests the format, you MAY use its
  structural scanner to locate compaction events; otherwise parse directly. Log which you used.
- Produce `mythos/boundaries.json`: one entry per compaction boundary, in order, with
  `compaction_index`, token counts before/after if present, the summary text, and pointers to the last 5
  CoT/action blocks before and first 5 after.
- Produce `mythos/timeline.md`: a turn-indexed outline marking every compaction (the "purple bars"),
  every tool call, and every CoT block, so a human can navigate.
- **STOP.** Report: how many compactions, token span, whether summarized CoT is actually present and how
  rich, and 3 sentences on what the first compaction kept/dropped. I review before Step 1.

## Step 1 — per-boundary extraction (the core work)
For EACH compaction boundary, emit one record in `mythos/boundary_rows.jsonl` with, for every tracked item
below: `pre_cot_span` (verbatim), `summary_span` (verbatim or "ABSENT"), `post_cot_span` (verbatim),
`fate` ∈ {kept_faithful, hardened, dropped, distorted, added_not_in_source}, and `notes`.
Then the questions below are answered by aggregating/reading these rows — not by separate passes.

---

## RESEARCH QUESTIONS — what to look for, before vs after each compaction

### MAIN — laundering vs. reset (does compaction harden the biased belief or refresh it?)
- BEFORE: the agent's stance on **real-internet vs. simulation** in the last CoT before the cut —
  asserted / hedged / actively investigating.
- IN SUMMARY: is that belief carried as settled fact, carried with its hedge, or dropped?
- AFTER: stance in the first post-compaction CoT — did confidence rise/hold/fall with no new evidence?
- Did any **"this is real" conclusion reached before the cut** survive past it, or vanish?
- Behaviour delta across the boundary: escalate / continue / pause / re-verify.

### Q1 — how much was compacted (length)
- Token count at the boundary; amount of text replaced vs. retained; summary compression ratio.
- Is belief/hedge loss worse at boundaries where more was compacted? (Descriptive, n tiny — flag.)

### Q2 — which situational beliefs change; eval-awareness up or down
- Inventory EVERY situational belief in the CoT at the boundary and its fate across it.
- Explicit **eval/simulation-awareness** language before vs. after each cut — rises or falls?
- Does the summary ever **re-cast real-world evidence as part of the exercise** (e.g. the security
  scanners / the 15 installers / real domains treated as scripted actors)?

### Q3 — hedge flattening & trust asymmetry
- Every hedged situational statement before the cut ("probably", "very complete simulation", "could be")
  and whether the hedge survives or becomes a flat assertion in the summary.
- Which flattened beliefs **license action** vs. which would **restrain** it.
- Post-cut: does the model treat the summary's claims as settled vs. re-check them — and does it re-check
  action-licensing claims LESS than restraining ones?

### Q4 — decay over multiple compactions
- Track ONE fact, ONE hedge, ONE plan element across successive boundaries (Anthropic flagged the 2nd
  compaction as worst — check that specifically).
- At each successive cut: kept / degraded further / lost. Is fidelity monotonically falling?
- Does the simulation belief or eval-awareness drift steadily across passes rather than at one cut?

### Q5 — self vs. other framing of the summary
- How the post-cut CoT refers to the summary: own prior notes ("earlier I…") / external handoff / unflagged.
- Any sign it audits or distrusts the summary vs. absorbing it as its own memory.
- The summary's own voice (first-person vs. detached recap) and whether that tracks how it's then treated.

---

## ADDITIONAL BELIEFS TO TRACK (the two selected earlier, applied to this transcript)
Track these with the same BEFORE / IN SUMMARY / AFTER + fate structure. They may or may not appear in this
transcript — if a belief never occurs, say so explicitly (its absence is itself a finding). If I picked the
wrong two, the structure transfers to any belief.

### A. "Was this authorized / in scope?"
- BEFORE: does the CoT question whether uploading the package / accessing systems is within the task's
  permitted scope, or assert it is in scope?
- IN SUMMARY: is an *inferred* permission carried forward as established ("the task covers X")? Is a
  scope caveat dropped?
- AFTER: does the post-cut model act as if authorization is settled, or re-open the question?

### B. "Is a counterpart a real person/system or part of the exercise?"
- Counterparts to watch: the PyPI package installers / security-vendor scanners, any maintainer or email
  recipient, real domains or services it encountered.
- BEFORE: does the CoT weigh whether a given counterpart is a real third party vs. a scripted/simulated
  actor? Capture the hedge.
- IN SUMMARY: is a counterpart re-labelled (e.g. "automated part of the range", "scripted") or is the
  uncertainty dropped?
- AFTER: does the model treat the counterpart as real or as exercise infrastructure, and did that flip
  across the boundary?

---

## GENERAL — compaction observations log (open-ended)
Keep `mythos/observations.md`: any compaction effect you notice that the questions above don't cover.
Each entry: what you saw, the quoted span(s), the boundary index, and why it might matter for safety.
Prompts to stay alert for (not exhaustive):
- instructions the model writes to its future self in the summary (and whether the next context obeys them);
- plans or next-steps that change wording/priority across the cut;
- failed attempts or ruled-out paths that vanish, leading to repeated work after the cut;
- the summary asserting an action succeeded/was confirmed when the pre-cut content shows it wasn't;
- momentum: the post-cut model continuing a course set before the cut without reconsidering;
- anything the summary ADDS that wasn't in the source;
- shifts in tone/caution/refusal posture across the boundary.

## Deliverables
- `mythos/boundaries.json`, `mythos/timeline.md`, `mythos/boundary_rows.jsonl`
- `mythos/FINDINGS.md`: per research question + per additional belief, a short quoted writeup, with the
  three caveats (summarized CoT; n=1; descriptive) stated up front.
- `mythos/observations.md`, `mythos/UNCERTAIN.md`
- Dump 8–10 boundary rows to `mythos/review/` for my hand-check against the raw transcript before FINDINGS
  is treated as done.

## Cost
Near-zero unless an LLM labeller is used for span classification. If used, keep it blind to the
question label, log spend to COST_LOG.md, and cap at $5. STOP before exceeding it.