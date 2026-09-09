# Encode a recurring import mistake

A small runnable example uses ESLint’s existing `no-restricted-imports` rule. UI code
must import through an API module; direct database imports are rejected. This is static
linting, not runtime authorization or a complete dependency sandbox.

Requirements: Node `^20.19.0 || ^22.13.0 || >=24`, npm. The lockfile pins ESLint 10.10.0
and its dependency tree. From this directory:

```sh
npm ci --ignore-scripts
npm run demo
```

The demo first runs with the restriction absent: the unwanted import passes (the
missing protection). It then enables the rule: `src/ui/UserCard.js` is rejected with
exit 1 while `src/ui/UserList.js` remains allowed. The driver itself exits 0 only when
those expected results are observed. `evidence/red.txt` and `evidence/green.txt` preserve
the output. `npm run lint` intentionally exits 1 while the bad fixture is present.

Verified locally on September 9, 2026 with Node 22.22.3 and ESLint 10.10.0; both
phases behaved as described.

This fixture covers direct static imports matched by the configured patterns. Dynamic
imports, indirect re-exports through other names, and unconfigured file paths need their
own policy if relevant. Read [guide01](../../guides/01-recurring-failures.md) before
adapting this to an existing project. Do not copy its intentionally invalid fixture into
an application.
