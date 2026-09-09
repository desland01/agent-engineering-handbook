# Feedback engineering: worked implementation

The video argues for replacing repeated manual corrections with reusable checks around [08:02](https://www.youtube.com/watch?v=xmGY276gEFY&t=482s). Theo adds that agents reduce the cost of implementing and testing a project-specific rule around [08:30](https://www.youtube.com/watch?v=xmGY276gEFY&t=510s). This does not establish that a rule prevents every instance permanently.

## A forbidden import

Suppose UI files repeatedly import a database module directly, bypassing the supported API. Inspect the project's existing linter before introducing a new plugin. ESLint's [no-restricted-imports](https://eslint.org/docs/latest/rules/no-restricted-imports) can express a restricted path and a message naming the approved replacement.

First show the recorded bad case passes without the restriction. Configure the smallest rule covering that case. Then show the bad case fails and a legitimate API import passes through the actual project lint command. If a custom AST rule is necessary, add meaningful fixtures for the intended pattern and legitimate exceptions using the linter's existing test harness. See the [custom rule tutorial](https://eslint.org/docs/latest/extend/custom-rule-tutorial).

Check both invocation and severity. A warning may be useful feedback without blocking delivery. Static imports are not every possible runtime import; state the rule's coverage honestly.

## A runtime outcome

For a chat feature, use independent authenticated browser contexts: one sends a unique message, the other must observe that exact message. This adapts Theo's Twitch story around [03:59](https://www.youtube.com/watch?v=xmGY276gEFY&t=239s); that test's source was not found here.

Preserve failure evidence deliberately. Playwright saves videos on context close; retention options and retry behavior differ. Consult [video recording](https://playwright.dev/docs/videos), [trace viewing](https://playwright.dev/docs/trace-viewer) and [retry outcomes](https://playwright.dev/docs/test-retries). A test that passes only on retry is a different observation from a first-attempt pass.

## A failed CI run

Let the agent obtain the actual run for its revision and read failed-step logs using [gh run view](https://cli.github.com/manual/gh_run_view). Preserve the first failure, classify its cause and observe the repaired revision. Keep communication and branch writes within the user's authorization. This useful loop appears in a sponsor segment; the sponsor's performance claims were not reproduced.
