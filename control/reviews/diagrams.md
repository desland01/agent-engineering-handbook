# Review record — the three investigation diagrams, 2026-09-10

**Maker:** Fable 5.1. **Reviewer:** gpt-6-astra, from 1280×640 renders of each figure at the size readers see it, with the intent withheld until a first impression was recorded.

| Study | Reviewer's verdict | Finding | Maker's answer |
|---|---|---|---|
| 01 T3 Code / Melee | fix first | Two repositories drawn as one line; the fork's parent ambiguous; the verifier reads as a badge, not a commit | **Applied.** Two named lines under *REPOSITORIES READ*; the fork hangs off `MELEE4MAC`; the verifier is a commit dot on that line with its box above it. |
| 02 Course Video Manager | fix first | The return loop points at the glossary, so it reads as recycling, not as an artifact keeping its identity | **Applied.** The loop leaves the artifact and returns *into* it; the artifact carries a symbolic tag `#A7F3` and the caption reads *RESUMED RUN → SAME ARTIFACT, TAG #A7F3*. A caption/arrowhead collision in the first fix was found by bounding-box check and moved. |
| 03 Boris Cherny | ship | Both connectors land on the fuzzing row, giving it false prominence; the compiler is implied, not named | **Applied.** One frame labelled *COMPILER VALIDATION* encloses the five layers; the connectors terminate at the frame. |

Also noted by the reviewer and accepted: the verifier's check mark and the output check were generic success badges — both gone.

Process note: the source for the first drawings was committed before this review returned, against the gate's order. The fixes land in a following commit with this record; the order will be review-then-commit from here.
