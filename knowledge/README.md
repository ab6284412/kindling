# Knowledge index

The map from each evergreen lesson to its drill and its curriculum stage.
Stages refer to [learning.md](../learning.md): 1 = language foundation,
2 = request/response core, 3 = API design & reliability, 4 = auth & security,
5 = state & storage, 6 = async work & concurrency, 7 = production, ops & scale.
"parallel" = the DSA/interview + AI track that runs alongside the stages.
All notes are AI-drafted; each credits the human author of its source.

| Lesson | Note | Drill | Last verified | Stage |
|---|---|---|---|---|
| Time-to-thought is a real model-selection axis | [time-to-thought.md](time-to-thought.md) · Alderson | [`## Drill` in that note](time-to-thought.md#drill) | 2026-08-03 | 7 |
| Retype generated code before keeping it | [retype-generated-code.md](retype-generated-code.md) · Sethi | [`## Drill` in that note](retype-generated-code.md#drill) | 2026-08-03 | 1 |
| DMARC authenticates the sender, not the content | [dmarc-caveat.md](dmarc-caveat.md) · SenderLedger | [`## Drill` in that note](dmarc-caveat.md#drill) | 2026-08-03 | 2 |
| Open-weights policy is a board-level topic | [open-weights-policy.md](open-weights-policy.md) · Anthropic | — (policy, not a skill) | 2026-08-03 | parallel |

## Rules for adding a row

- New note without a drill = summary only; add a drill when the lesson can be
  practiced, or mark the drill cell `—` and say why.
- A note's `Last verified` date changes when you re-read the source and confirm
  the claim still holds. An index row with a stale date is the freshness alarm.
- Every note must carry `Provenance:` and `Credits:` — the index mirrors the
  credit (author surname) so a reader can trace at a glance.
