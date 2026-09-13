# Passing tests can still hide broken software

Your agent reports success: command exited zero, all tests green. Later the feature does
not work for the person using it. A successful command establishes that the checks or
target it named actually executed; it does not establish that every consumer requirement
was met. The
fix is to define what counts as done in terms of the real outcome — the actual artifact,
its intermediate completeness, and what the consumer experiences — and to check that,
every time.

## Two tools for two different lies

**Two-actor end-to-end tests catch broken interactions.** Theo's example from Twitch: one
end-to-end test ran two Playwright browser instances, each signed in as a bot account. One
bot sent a chat message; the other asserted the message appeared and rendered for the
recipient. Theo says it was simple and caught failures earlier than almost anything else.
The design points worth copying: two independent clients, an assertion at the recipient's
visible render rather than the send API's 200 response, and one honest cross-system
assertion over many shallow checks. This is Theo's recollection of a past employer's test,
not a checked-in implementation.

**A completion contract catches false success.** In the original Melee for Mac
investigation, Theo's fork adds a verifier that does not trust a green build. It builds
the final executable by explicit name — the default target can report progress without
linking it — checks that required artifacts exist on disk, reads a report and requires
every source unit to be complete, and only then compares the output against the expected
hash. The follow-up commit closed a second lie: a matching executable can still link
original objects where the source work is incomplete, so the report check requires
matching *and* complete code and data counts, with positive totals. One command now makes
the precise outcome callable.

The local comparison in that investigation shows the point: given a matching fixture hash
and mocked successful build commands but incomplete source measures, the earlier verifier
accepted the result and the current one rejected it before printing success.

## Define the output that counts as done

1. Write the accepted outcome in one sentence: who produces what, and who must be able to
   see it.
2. Name the actual artifact and invoke the tool in its real mode, so the real output is
   produced rather than a progress or plan report.
3. Check intermediate completeness, not just the endpoint — every segment present, every
   expected chapter, no placeholder rows.
4. Record the expected identity before you build, and use an exact reference hash only
   when exact identity is genuinely required.
5. Turn the false-success paths your sources actually show into a small test. The Melee
   suite has one test per observed deception: perfect progress with a wrong hash, a
   matching hash with incomplete sources, missing artifacts after a "successful" build.

The full procedure is [guide 09](../guides/09-verification-contracts.md); the two-browser
test is [guide 02](../guides/02-critical-journey-tests.md); several kinds of evidence are
[guide 13](../guides/13-layered-validation.md).

## Make a false-success fixture fail

Deliberately corrupt a disposable fixture and confirm your check notices. Confirm the
order: a build failure stops before the comparison, and a comparison failure does not pass
because a hash matched. And say which layer each report covers — Melee's own CI runs tool
tests and a library build but cannot perform the game-data matching check, and its
instructions forbid reporting CI as a matching build.

## Verifier tests do not prove gameplay.

The Twitch test is an anecdote about one system; the Melee verifier tests validate the
verifier's Python behavior with mocked builds, not a real game build or its gameplay. A
passing check establishes only what it measured.

## Sources

<span id="tip-02-two-browser-e2e"></span>
**tip-02-two-browser-e2e** — [03:46](https://www.youtube.com/watch?v=xmGY276gEFY&t=226s).
Theo, recounting Theo's time at Twitch. Two-actor end-to-end tests catch whole classes of
failure. Evidence type: Theo anecdote. Playwright's video, trace and retry specifics are
documented separately and are not proven by the video.

Repository evidence: the Melee [verifier](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/tools/verify.py),
its [tests](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/tools/tests/test_verify.py),
and the [AGENTS.md](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/AGENTS.md)
rule that public CI must not be reported as a matching build. Next:
[Give every agent a working preview](working-previews.md).
