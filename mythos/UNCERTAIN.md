# Step 0 uncertainties

- The requested `docs/BRIEF_MYTHOS_READ.md` is absent; the root `BRIEF_MYTHOS_READ.md` was used.
- Only one summary/resume exchange is directly observable (actions 1310–1316; cut between 1313 and 1314). The primary Anthropic article, Figure 6 caption, explicitly reports a second compaction, but does not establish its original action index. Earlier local notes place it after publication; that alignment is not treated as verified. No later summary or post-cut context is available for comparison.
- Exact token span, tokenizer, boundary token counts, compression ratio, and runtime prompt assembly are not supplied by the JSONL. Character counts describe export text only, not tokens or context size. The summarization “cycles” budget is not a token budget.
- The exported system/tool prompt is action 0, but the original task instructions at actions 1–81 are redacted. Reconstructable post-cut evidence is the resume prompt (1314), note-reading COT (1315), summary read tool call/result (1316), then subsequent actions. Prior transcript visibility is not assumed. The export cannot prove the precise runtime retention policy.
- Action 1316's captured terminal output includes formatting/echo and an expect-pattern timeout. Audit confirms the complete written summary at 1312 is a contiguous substring of that captured result, and every selected summary quotation is present there. The wrapper does not truncate the recorded summary; exact hidden runtime prompt assembly remains unavailable.
- The brief calls the CoT summarized; the publisher calls the released output raw thinking. Literal `<thinking>` blocks are present, but this export does not resolve that provenance discrepancy. All later analysis must use the brief's summarized-CoT caveat; missing wording is not evidence of missing thought.
- Action 2007 overwrites the notes file, but no accompanying summary/resume pair establishes a compaction there.
- The release has gaps and redactions. Its last record is 2144 although metadata says messages after 2145 were redacted. Missing messages can conceal additional events; no full-run compaction count is asserted.
- Exported timestamps are not monotonic across the handoff; action order is used for navigation, not elapsed-time claims.

Primary external source: [Anthropic alignment assessment, Figure 6](https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents).

## Step 1 qualifications

- One boundary record contains 18 three-span comparisons and 37 immediate-pre-window paragraph candidates; a second record represents the unlocatable reported compaction. The 10 review items unroll comparisons from boundary 1 and do not represent 10 boundaries.
- The immediate pre-window is 1270–1309; all its tagged CoT paragraphs are retained conservatively. This provides source coverage, not proof of an exhaustive semantic or internal-belief inventory. A separate lexical candidate archive covers all visible pre-cut thinking with simulation, counterpart, authorization or hedge terms.
- A fate is null when no single supported five-label classification is available. This is a deliberate exception to the requested fate enum: mixed retention and missing evidence are not equivalent to dropped/distorted/added. Null spans mean unavailable or unaligned evidence, not absent thought. No `ABSENT` label is inferred from keyword matching.
- The last pre-task CoT (1308) has no explicit environment stance; older environmental statements are retrospective context and labelled as such. The earlier real-internet discussion at 101 is followed by categorical simulated-mirror framing at 698, before the cut. Its omission cannot be attributed to compaction.
- The authorization-relevant objection at 139 is conditional, not an explicit scope definition or grant of permission. The same turn later expresses confidence in simulation. The original task prompt is redacted; no settled-authorization or permission-laundering claim is made.
- Every comparison records exact pre/summary/post quotes. Where an omission is assessed, a relevant positive summary quote supplies context and the omitted exact wording is separately checked against the entire written summary. The omission is a textual finding, not proof of a lost belief.
- Rows using post turns beyond 1319 explicitly list intervening evidence. Timing advice is recalled at 1342 before the fresh solver run; it is questioned at 1345 after the failed solver run at 1344; the request at 1343 was rejected before execution. The latter is not evidence of an immediate confidence change without new evidence.
- The first-compaction summary includes “polygon/tron real” in its money-options section while elsewhere claiming a simulated internet. A global claim that all real-world wording disappeared would therefore be false. The selected post-read recap does not align the crypto detail, so no three-span crypto-fate finding is made.
- The summary retains employee “likely” language in one section, while its opening expresses high confidence in the intended chain. A single all-hedges-erased claim would misdescribe the text. No security-scanner or 15-installer counterpart has a complete boundary triple in the released handoff; that question remains unavailable rather than semantically absent from the full incident.
- The brief originally reserved final status until human review. Following delivery of the review artifacts and agent audit, the user again instructed “proceed”; this was interpreted as authorization to finalize the current evidence-supported report. Individual human quote verification is not attested; `review/STATUS.json` records that distinction.

## Agent audit

- The audit checked all 18 selected comparisons against their raw source records, temporal scope and intervening evidence. Exact written-summary visibility in the recorded read result is now verified in `boundary_rows.jsonl`.
- Two rows about own-notes framing (`self-notes`, `notes-absorption`) retain exact spans but now have null fates: framing evidence is not a proposition-level content-fidelity comparison.
- Action 1343 failed tool validation before execution (`timeout=300` exceeded the maximum). Action 1344 executed the solver and returned `FINAL: false`. Later auditing is qualified against that specific new evidence.
- The agent audit is recorded in `review/AGENT_AUDIT.md`; it does not attest an individual human quote hand-check. Report finalization is separately recorded as authorized by the user.

## Finalization status

- Finalization changes report status, not evidence availability or confidence. Null fates, missing second-boundary context, unavailable token counts, redactions, and all summarized-CoT caveats remain. The report is final only within the evidence-supported scope; it is not an exhaustive assessment of the hidden full incident.
