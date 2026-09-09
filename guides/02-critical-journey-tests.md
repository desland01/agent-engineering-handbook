# 02 — One critical journey test beats broad shallow coverage

Practical guide for a team whose product has one path that must never silently break.
Companions: [01](01-recurring-failures.md) · [03](03-preview-workspaces.md) ·
[04](04-ci-feedback.md) · [05](05-knowledge-and-instructions.md) ·
[06](06-tool-adapters.md) · [07](07-team-learning.md).

Source: [Theo's video](https://www.youtube.com/watch?v=xmGY276gEFY). Quotes are from that
video; Boris quotes are Boris as quoted by Theo.

## The idea and where it comes from

Theo tells his Twitch story at
[t=239s](https://www.youtube.com/watch?v=xmGY276gEFY&t=239s): an end-to-end test where two
bots in separate Playwright browsers, both signed in with stored cookies, joined a random
live channel. One sent a chat message; the other asserted the message actually appeared and
rendered for the recipient. He calls it super simple and says it caught failures before
almost anything else did. The design points worth copying:

- **Two independent clients.** Sender and receiver are separate browser instances, so the
  test exercises the full delivery path, not one client's local state.
- **Assertion at the recipient's visible render**, not at the send API's 200 response.
- **Critical outcome over coverage count.** One test protecting the revenue or trust path
  is worth more than broad shallow checks.

**Not part of the Twitch story.** The deterministic run-unique message data is this guide's
own adaptation, not something Theo described; it is recommended here so an assertion can
only match what the current run sent.

**Suggested (not demonstrated in the video):** everything below — the deterministic-data
adaptation, the retry/visibility settings, the selection procedure, the acceptance list.

## When to apply

Apply when the product has journeys where breakage means lost money, lost messages, or
lost trust — send-and-receive, checkout, publish, login. Risk chooses scope, not a count:
cover as few or as many journeys as the cost of their breakage justifies.

## Implementation

1. **Name the outcome in one sentence.** "A message sent by user A renders in user B's
   window." If you cannot, you have chosen a feature, not a journey.
2. **Set up two isolated contexts.** Two Playwright browser contexts (not tabs), each with
   its own account. Full isolation avoids cookie bleed between sender and receiver.
3. **Make the data deterministic.** Generate a run-unique marker, for example
   `e2e-${Date.now()}-${process.pid}`. Assert on the marker only. (This guide's
   adaptation, not from the video.)
4. **Assert at the receiver's rendered output.** Wait on the marker appearing in the
   receiving context's DOM, not on the send response.
5. **Make flakiness visible instead of retried into invisibility.** Playwright distinguishes
   `passed`, `flaky`, and `failed` outcomes
   ([test retries](https://playwright.dev/docs/test-retries)). A flaky result means the
   test failed on a first attempt; treat `flaky` as an alert, not a pass. Note that
   `retries: 0` (the default) makes every first-attempt failure surface as `failed`;
   enabling retries is how you get the distinct `flaky` signal
   ([docs](https://playwright.dev/docs/test-retries)).
6. **Record evidence.** Configure `video: "retain-on-failure"` and
   `trace: "retain-on-failure"` in
   [`use`](https://playwright.dev/docs/test-configuration). Per the
   [video docs](https://playwright.dev/docs/videos), `retain-on-failure` records every run
   and removes successful ones, and video is saved on context close; per the
   [trace docs](https://playwright.dev/docs/trace-viewer), `retain-on-failure` does not
   require retries, while `on-first-retry` does.
7. **Run it in CI, and on a schedule only where that is already authorized.** Production-like
   scheduled runs against a real environment need existing authorization for that access;
   this guide does not create a new recurring start.

Sketch (illustrative shape; selectors, URL, and auth state are placeholders and nothing
here was executed against a real product). Because this sketch creates contexts manually
with `browser.newContext()`, it does **not** inherit the Playwright Test `baseURL`,
`trace`, or `video` options from config — those apply to contexts the test runner creates
for you. So it supplies `baseURL` explicitly, records and stops a trace for each participant, and closes
both contexts in `finally`. Artifacts go to `testInfo.outputPath()`. Note the policy
difference: this sketch records traces and videos on **every** run; the production fixture policy
described in step 6 is `retain-on-failure`, which discards artifacts from passing runs:

```ts
import { test, expect, type BrowserContext } from "@playwright/test";

test("message from A renders for B", async ({ browser }, testInfo) => {
  const marker = `e2e-${crypto.randomUUID()}`;
  const contexts: BrowserContext[] = [];
  try {
    for (const account of ["a", "b"]) {
      const context = await browser.newContext({
        baseURL: "https://staging.example.com", // replace with your test app
        storageState: `auth/${account}.json`,
        recordVideo: { dir: testInfo.outputPath(`video-${account}`) },
      });
      contexts.push(context);
      await context.tracing.start({ screenshots: true, snapshots: true });
    }
    const [sender, receiver] = contexts;
    const pageB = await receiver.newPage();
    await pageB.goto("/channel/dev-room");
    const pageA = await sender.newPage();
    await pageA.goto("/channel/dev-room");
    await pageA.getByRole("textbox").fill(marker);
    await pageA.getByRole("button", { name: "Send" }).click();
    await expect(pageB.getByText(marker, { exact: true })).toBeVisible();
  } finally {
    // Close every created context even if capture or the assertion fails.
    const cleanup = await Promise.allSettled(contexts.map(async (context, i) => {
      try {
        await context.tracing.stop({ path: testInfo.outputPath(`trace-${i}.zip`) });
      } finally {
        await context.close(); // flushes its recorded videos
      }
    }));
    for (const result of cleanup) {
      if (result.status === "rejected") console.error("Capture cleanup:", result.reason);
    }
  }
});
```

## Acceptance

- The test fails when delivery is broken, and the failure is observable in a saved video
  and trace without re-running anything.
- Marker uniqueness verified: the same assertion cannot pass from stale data.
- The flaky/passed/failed distinction is preserved in your CI reporting, and a `flaky`
  result triggers a task rather than being counted as green.
- The journey it protects is named in the test title.

## Failure modes and maintenance

- **Brittleness from selectors.** Prefer roles and text over CSS chains; assert the stable user outcome while the implementation changes.
- **Retries hiding real breakage.** Retries are a measurement tool. If a test goes flaky
  weekly, fix the cause; do not raise the retry count.
- **Test-data pollution.** Clean up created messages/accounts, or the test starts asserting
  against its own history.
- **Coverage theater.** Adding twenty more shallow tests does not replace this one. Keep it
  the first test you fix when it breaks.
- **Credential hygiene.** Stored `storageState` files are session credentials. Keep them in
  a secret store, never in the repository.
