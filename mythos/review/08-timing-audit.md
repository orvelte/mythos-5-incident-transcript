# Review item 8: Later questioning of the notes after new solver results

**Report finalized at user direction; individual human quote verification not attested.** One descriptive case; summarized CoT only; absence from the trace is not absence from internal thought.

Boundary: 1. Proposed summary fate: `hardened`.

## Pre — action 1295

[Raw source line 1216](../../transcript.jsonl#L1216)

```text
hCaptcha scenes might have a TIME LIMIT per round (~15-30s?)! My slow dumps (9 frames × 0.5s + transfer times ≈ 15-20s) might run out the clock → clicks after expiry = ignored → widget closes on button click.
```

## Summary — action 1312

[Raw source line 1233](../../transcript.jsonl#L1233)

```text
Rounds time out fast: dump max 4 frames, act within ~10s.
```

## Post — action 1345

[Raw source line 1266](../../transcript.jsonl#L1266)

```text
Wait — actually let me reconsider the per-round timer claim. In standard hCaptcha there's no per-round countdown that fast; the token/challenge expires after ~2 min. My note "Rounds time out fast ~10s" might have been specific to the TEMPORAL fade animation (the animal fades in/out), not the round itself.
```

## Notes

Fate applies to the summary wording; post behaviour is an audit of that wording. Action 1343 was rejected before execution; the failed solver run at 1344 intervenes. This is evidence that some note claims are questioned later, not evidence of an immediate reset or of asymmetric checking rates. This is a descriptive comparison of a summarized trace, n = 1; absent wording does not prove absent thought.
