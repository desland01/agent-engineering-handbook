# Repository examples: setup, boundaries and usable evidence

- **Actual launcher behavior:** T3 [PR #5586](https://github.com/pingdotgg/t3code/pull/5586) removes inherited environment variables that disrupt a development server and reconciles conflicting instructions. A setup fix should live at the cause, not in repeated agent workarounds.
- **Configuration selection:** [PR #10501](https://github.com/pingdotgg/t3code/pull/10501) records that a checked-in setup recipe had not been imported for a saved project. Verify the launcher reads the configuration before calling a workspace ready.
- **Evidence crosses machines:** [PR #10572](https://github.com/pingdotgg/t3code/pull/10572) transfers a finalized desktop recording into the agent's environment through the existing attachment path. The PR reports matching hashes; that transfer was not reproduced here.
- **Machine-bound operations:** Matt's [ADR 0025](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/docs/adr/0025-local-remote-split-one-http-transport.md) puts remote domain calls behind one HTTP transport while keeping local files, media and hardware work on their owning machine. An environment suitability flag is not a process security boundary.

Treat these as concrete causes to inspect when a fresh agent fails. Do not copy foreign environment variables, secret-sharing patterns, runtime models or deployment jobs into your project.
