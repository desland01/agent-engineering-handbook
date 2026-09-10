# Review record — the nineteen idea pages, 2026-09-10

**Maker:** gpt-6-astra (writer run, 76 sections from `evidence/video-tips.json` and
`evidence/video-research.md` under the grounding rules in its task).
**Reviewer:** Fable 5.1 — a different route from the maker, as the design review gate requires.

## What was checked

1. **Mechanical (`build/check.py`).** Four sections per page; no heading is a schema label;
   no heading repeats on more than two pages; every section has at least three sentences.
   PASS across 19 pages after integration (it was red with 76 label headings before).
2. **Grounding.** Every sentence (230) scanned for names, numbers and file references not
   present in that tip's fields or its research passage: **0 flagged**. This is a
   heuristic, not a proof of meaning; it catches invented specifics, not invented
   framing.
3. **Attribution.** Speaker strings preserved per the writer's choice log (sponsor segment
   kept as sponsor; Boris-as-quoted kept as such; Theo's speculation kept as speculation).
   Spot-read: tip-03 in full — heading "Agent multipliers" matches the owner's example;
   the `fit` section states the unmeasured magnitude rather than hiding it.
4. **The writer's own log** (`RESULT.md`) records a wording decision for all nineteen tips,
   each choosing the more qualified reading where the extraction and the research differed.

## Findings

None blocking. One observation for the next pass: several `useful` sections close with a
"do not …" sentence that reads as a template move across pages; it is grounded each time,
but a later edit could vary the form.

## Maker's answer

Not applicable — no findings to apply. Integrated at this commit.
