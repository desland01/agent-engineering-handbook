# A delegated worker can drive a browser, and a run that cannot do what it was told fails

2026-09-11. Deliverable for the Nautilus runtime. `PLAN.md` beside this file is the design
and the evidence that prompted it. This directory is the change; it lives here because the
runtime source tree at `~/Documents/Codex/2026-09-04/ca/outputs/nautilus` carries 5,460 dirty
files belonging to another session, and nothing here writes into it.

## Apply this after `control/runtime/skill-selection`

Both deliverables define contract **version 5**: `skill-selection` adds the required
`skillPlan`, this one adds the optional `network` and external `allowRead`. They are one
contract version, not two, because neither has shipped and a release admits them together.
The patch here is cut against *original + `skill-plan.patch`* and will not apply to a tree
without it. Order: `skill-plan.patch`, then `worker-egress.patch`.

Merging them found a real defect in the other deliverable, fixed here: it generalised the
schema's version gates but left `capsule-admission.mjs` and `task-lifetime.mjs` pinned to
`capsule.version === 4`, so a version 5 capsule with `limits.maxRequests: null` parsed and
was then **refused at admission** with `capsule_unlimited_requests_not_authorized`, while the
identical version 4 capsule was admitted. Measured before and after; every long-running
version 5 worker would have hit it. The version lists `NO_DEADLINE_VERSIONS` and
`UNLIMITED_REQUEST_VERSIONS` replace those literals so a contract version inherits what the
previous one had.

## What is in this directory

- `PLAN.md` — the measured failure, the four enforcement points, the approach and the
  alternatives rejected.
- `worker-egress.patch` — `git diff` against original + `skill-plan.patch`. 15 files,
  +938/−28. Apply from the runtime repo root with `git apply <path>/worker-egress.patch`.
- `qa-capsule.json` — the capsule the blocked browser-QA assignment needs, written against
  the merged contract. It is refused by the currently installed release, by design.

## What the change does

**The capsule may declare what it needs, within a release ceiling.**

- `capsule-schema.mjs` — contract version 5. Optional `network: {allowedDomains,
  allowLocalBinding}`; `allowRead` entries outside the workspace are now expressible. Hosts
  are exact or one leading wildcard label; `*`, a scheme, a path or an empty list is refused
  at parse. The version lists `NO_DEADLINE`, `UNLIMITED_REQUESTS` and `EGRESS` replace the
  scattered `version === 4` literals, so version 5 inherits every version 4 allowance instead
  of silently dropping one.
- `capsule-admission.mjs` — `capsuleSandboxScopes` takes the release ceiling as a third
  argument and returns a real network block. A read outside the workspace is granted only
  inside an Anchor `readableRoots` entry and only as a read; a host is granted only where an
  Anchor entry covers it. Refusals name the thing to change:
  `capsule_network_widens_anchor: <host>`, `capsule_local_binding_widens_anchor`,
  `capsule_read_widens_anchor: <path>`, `capsule_network_unavailable_in_release`. With no
  ceiling in the release, the previous `capsule_read_widens_runtime` refusal is unchanged.
  `childSubsetViolations` gains a `network` dimension: a child cannot reach a host its parent
  does not hold, and cannot claim local binding the parent lacks.
- `release.ts` / `types.ts` — `validateAnchorSandbox`. A malformed ceiling refuses the
  release rather than resolving to "grant nothing". A wildcard directly over a public suffix
  (`*.com`, `*.co.uk`) is refused: a ceiling has to name what the business actually reaches.
- `capsule-runtime.mjs` — the ceiling is measured into the binding facts, so an ungranted
  egress fails `scopes_narrow_runtime` and refuses the launch. The admitted run carries its
  network scope beside its filesystem scopes, and the admission event records it.

**The granted run can actually reach the host.**

- `egress.mjs` (new) — `egressTarget` decides one CONNECT against the admitted list;
  `attachEgress` tunnels it. A remote host is reachable on 80/443 only. A granted local
  service is reachable on the port it listens on, because that grant exists so a run can
  drive a dev server. A loopback or RFC1918 target needs `allowLocalBinding`, and a public
  hostname that *resolves* onto a local address is refused after resolution — the ceiling
  grants a name, never whatever that name points at today. Every attempt, allowed or
  refused, appends an `egress_request` record with host, port, verdict and byte count.
- `provider.ts` — the model endpoint's own rules are untouched: it still answers nothing but
  `POST /v1/messages*`. Its CONNECT handler, previously an unconditional 403, now delegates
  to `attachEgress` with this run's admitted hosts; with no grant the 403 is byte-identical.
  Egress rides the existing provider port rather than a second one because the sandbox routes
  all non-loopback traffic to `httpProxyPort`, and moving that port would break the model
  path's own loopback allowance. `PLAN.md` proposed a separate port; this is the correction.
- `runtime.ts` — the run's `SandboxRuntimeConfig.network` comes from the admitted capsule
  scopes instead of a hardcoded empty literal.

**A run that could not do the work cannot be accepted.**

- `ticket-harness.ts` — a ticket may declare `requires: {route, capsule: {network, read,
  tools}, receipts}`, validated when the plan is read. Four gates, one classification:
  1. *Before launch*: the capsule is parsed with the real schema parser and compared with
     `requires.capsule`. A gap blocks the ticket and **no worker starts**, so the run never
     gets the chance to substitute something else.
  2. *After the run*: an `egress_request` with `allowed:false`, or any boundary refusal in
     the record, outranks a `completed` status and its written artifacts.
  3. *Route*: artifacts produced by a route the ticket did not name are refused, naming both.
  4. *Evidence*: a `requires.receipts` key that is missing or empty fails as
     `receipt_missing: <key>` — a missing capability, not a quality defect, so it never
     routes to repair where a model could rewrite its way past it.
  All four block with `capsule_insufficient` and record the capsule revision judged. That
  block is the deliberate inverse of `definition_changed`: the ticket returns to the queue
  when the **capsule** changes and only then. Rewriting the task to describe a workaround,
  re-running, or editing the checker leaves it blocked.

No existing check was weakened. Two expectations moved with the contract version:
`capsule.test.mjs` now probes `CAPSULE_SCHEMA_VERSION + 1` instead of the literal `5` it used
as an out-of-contract version, and `capsule-role.test.mjs` expects versions 1–5 with 6 refused.

## Verified

Staging copy of the runtime tree with its real `release/`, `node_modules`, `vendor` and
`authority`; an identical baseline copy with only these twelve files reverted and the five new
files removed.

- **New checks, written before the change**: `capsule-egress` 21, `capsule-egress-tunnel` 9,
  `ticket-capsule-gate` 8, `sandbox-anchor` 4 — 42/42 with the change. Run against the
  unchanged runtime in the baseline copy they are 6 pass / 25 fail, so each one measures the
  correction rather than restating what the runtime already did. (The 6 that pass at baseline
  are the cases asserting unchanged behaviour: the old `read_widens_runtime` refusal, a
  release with no ceiling, and the malformed-declaration refusals.)
- **Full suite, matched environments**: baseline 1,163 pass / 139 fail; with the change 1,175
  pass / 139 fail. The two failure sets are **identical** (`diff` clean), so nothing that
  passed before fails now. The 139 are pre-existing in this staging tree (Electron and
  `release_mismatch` environment failures, unrelated to these files). The +12 are the two new
  root-level suites; `tests/capsules/` is outside the `npm test` glob and was run per file.
- **Per-file, both trees**: `capsule` 39, `capsule-runtime` 26, `capsule-role` 15,
  `capsule-chart-context` 5, `ticket-harness` 43, `ticket-packet` 10, `ticket-owner-launch` 2,
  `task-lifetime-anchor` 1, `worker-limits` 4, `provider` 3, `model-output-limit` 4 — same
  counts on both sides, zero failures.
- **Both deliverables applied together**, which is how they will ship: `skill-plan` 11,
  `capsule-egress` 21, `capsule-egress-tunnel` 9, `ticket-capsule-gate` 8, `sandbox-anchor` 4,
  `capsule` 39, `capsule-runtime` 26, `capsule-role` 15, `capsule-chart-context` 5,
  `ticket-harness` 43, `ticket-packet` 10, `task-lifetime-anchor` 1, `worker-limits` 4,
  `provider` 3, `release` 8 — 207 pass, 0 fail, `tsc --noEmit` clean. On that branch a
  version 5 capsule declaring both a `skillPlan` and a `network` parses, keeps its
  no-request-cap allowance and carries its admitted hosts.
- `tsc --noEmit`: 0 errors, the same as the unmodified tree.
- The patch applies clean to the runtime tree (`git apply --check`).

What this evidence does **not** show: no live run has used an egress grant, because that needs
a release carrying a `sandbox` ceiling, and the installed release has none. The tunnel is
proven against a local origin server in `capsule-egress-tunnel`, not against the internet.

## Not done here, and why

**Shipping it.** A runtime release is runtime code plus release content. This needs the
runtime rebuilt (`npm run build`) and installed, and it needs a release whose `anchor.json`
carries a `sandbox` block naming the hosts and readable roots the business actually uses.
Both are owner operations that produce a new release digest. Until that happens, the installed
release refuses every version 5 capsule that declares egress with
`capsule_network_unavailable_in_release` — which is the correct behaviour for a release that
was never granted the ceiling, not a failure of this change.

**The Linux isolation path.** `isolation.configuration(config)` post-processes the sandbox
config on Linux. Everything here was measured on macOS; the Linux boundary needs its own
measurement before anyone claims it enforces the same thing.

**The browser QA that prompted this.** It stays blocked. Re-running it against a substitute
route would be the exact behaviour the checker gate now refuses.
