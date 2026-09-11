# A delegated worker can drive a browser, and a run that cannot do what it was told fails

2026-09-11. Deliverable for the Nautilus runtime. Two coupled changes: the capsule gains a
declarable egress and read scope so browser QA can run inside the boundary, and the ticket
harness refuses a run that worked around a scope it did not have.

## What happened, measured

A browser-QA assignment was delegated to `gpt-6-astra` through the fleet entry (run
`654bf5a3-6af5-434b-9430-dc8d7c96f0bd`, capsule `astra-visualizer-qa-probe`). The capsule
was admitted. Inside it:

| Probe | Result |
| --- | --- |
| `curl https://www.rangerpainting.com/resources` | `curl: (56) CONNECT tunnel failed, response 403` |
| `require('<repo>/node_modules/playwright')` | `MODULE_NOT_FOUND` |
| `ls <repo>/apps/ranger-production/src/app` | `Operation not permitted` |
| Chromium launch + navigate | never reached; module resolution failed first |

Nothing in the boundary was broken. Every refusal is the current design working as written.
The failure is that the assignment was impossible to complete and the run still ended
`status: completed`, and the parent then proposed to do the work itself. That substitution is
the defect this deliverable removes.

## What already exists

Four enforcement points, all in the installed release and byte-identical to the source tree
at `~/Documents/Codex/2026-09-04/ca/outputs/nautilus` (checked with `diff`; only `runtime.ts`
differs, by an unrelated `nextTask` addition ahead of the release):

1. `src/capsule-schema.mjs:41` — the declaration contract is an explicit field list and
   refuses unknown fields. There is no network field to declare.
2. `src/capsule-admission.mjs:231` — `capsuleSandboxScopes` refuses any read scope not
   contained in the runtime write scope (`capsule_read_widens_runtime`), and line 236 returns
   a fixed `network: {allowedDomains: [], deniedDomains: [], allowLocalBinding: false}`. The
   capsule cannot influence either.
3. `src/runtime.ts:235` — the run's sandbox config hardcodes the same empty network literal;
   line 316 sets `config.network.httpProxyPort = provider.port`, so every non-loopback request
   is funnelled into the model provider server.
4. `src/provider.ts:145` — that server answers every CONNECT with `403 Forbidden`, and
   line 66 refuses any path that is not `/v1/messages*`. It is a strict model endpoint
   doubling as a deny-all proxy. This is the 403 the probe met.

Model traffic does not use that proxy path: `runtime.ts:314-316` sets
`ANTHROPIC_BASE_URL=http://127.0.0.1:<providerPort>` with `NO_PROXY=127.0.0.1`, so model
requests go direct to loopback and `httpProxyPort` governs everything else. That separation is
what makes this change small.

The sandbox itself already supports what is needed. `@anthropic-ai/sandbox-runtime@0.0.75`
takes `network.allowedDomains` as a real proxy allowlist
(`dist/sandbox/sandbox-config.d.ts:597`), and `runtime.ts:235` already forwards
`capsuleRun.scopes.allowRead` into `filesystem.allowRead`, where it carves exceptions out of
the `/Users` denyRead. No new dependency is required for either half.

On the harness side, `src/ticket-harness.ts` already owns acceptance: `classifyWorkerOutcome`
(line 603) maps an outcome to one of four classifications, `INFRASTRUCTURE_REASON` (line 601)
pattern-matches reasons, `evaluateEvidence` (line 626) reads the checker's evidence file, and
`definitionsUnchanged` (line 807) freezes the task, capsule and checker digests so a changed
definition blocks the ticket (line 1186). There is no concept of "this ticket requires a
capability the capsule does not grant", so a scope-starved run reaches the checker and is
judged on whatever text it produced.

## Approach

**Chosen: declare egress on the capsule, ceiling it in the Anchor, and gate the ticket on the
declaration before any attempt is launched.**

Two alternatives were considered and rejected:

- *Teach the model provider proxy to tunnel CONNECT for allowed hosts.* Smallest diff, worst
  design: it merges the model capability endpoint with general egress, so every future
  browsing grant is also a change to the file that authenticates model requests. Rejected on
  blast radius, not on effort.
- *Grant the worker the repository as its workspace so reads and toolchain come free.* Works
  for reads, does nothing for network, and buys read access by handing a QA worker write
  access to the whole repository, because `capsuleSandboxScopes` requires `allowWrite` to both
  contain the workspace root and sit inside it. Rejected: it widens write authority to solve a
  read problem.

The chosen approach keeps the model path untouched, keeps the default deny-all, and makes the
grant explicit, narrow, bounded by the release, and visible in the run record.

### Minimal viable slice

Capsule `network` declaration + Anchor ceiling + runtime wiring + the harness precondition
gate. That alone unblocks browser QA and stops the substitution, because a ticket whose
capsule lacks the capability never launches.

### Longer horizon

The capability receipt in the checker (below). Without it a worker with a *granted* scope can
still write a report it did not measure. With the MVP alone that is possible; with the receipt
it is not. The receipt is cheap for the browser case, so it ships in the same slice.

## Interface contracts

### 1. Capsule declaration, version 5

Version 4 is unchanged and keeps refusing unknown fields. Version 5 adds one optional field
and one relaxation. A version 5 capsule that declares neither behaves exactly like version 4.

```jsonc
{
  "version": 5,
  // ... every version 4 field, unchanged ...

  // NEW, optional. Absent means today's behaviour: no egress at all.
  "network": {
    "allowedDomains": ["www.rangerpainting.com"],  // exact hosts or "*.example.com"; no bare "*"
    "allowLocalBinding": false                      // true only to reach a local dev server
  },

  // RELAXED. Entries outside workspaceRoot are now permitted, read-only, and only when
  // contained in an Anchor readable root. Unchanged for every existing capsule.
  "allowRead": ["/Users/thebeast/ranger-painting-full-build"]
}
```

Refusals, each a distinct message so the remedy is unambiguous:

| Condition | Error |
| --- | --- |
| `network` present on version ≤ 4 | `capsule_network_unsupported_version` |
| `allowedDomains` empty, `"*"`, or not a host pattern | `capsule_network_pattern_invalid` |
| a domain outside the Anchor ceiling | `capsule_network_widens_anchor: <domain>` |
| `allowLocalBinding: true` without the Anchor permitting it | `capsule_local_binding_widens_anchor` |
| an `allowRead` entry outside every Anchor readable root | `capsule_read_widens_anchor: <path>` |
| the release Anchor carries no `sandbox` block at all | `capsule_network_unavailable_in_release` |

The last one matters: an older release refuses a capsule that asks for egress rather than
silently ignoring the field.

### 2. Anchor ceiling, `release/anchor.json`

```jsonc
"sandbox": {
  "version": 1,
  "readableRoots": ["/Users/thebeast/ranger-painting-full-build", "/Users/thebeast/Projects"],
  "network": { "allowedDomains": ["www.rangerpainting.com", "localhost"], "allowLocalBinding": true }
}
```

The Anchor is the ceiling and the capsule narrows it; the capsule can never widen it. Absent
`sandbox`, every existing behaviour is unchanged and every egress declaration is refused.
Because the Anchor is sealed, changing this list is a release operation with a new digest —
which is the intended cost of granting a new destination.

`validateAnchorSandbox` in `release.ts` refuses a malformed ceiling outright, so a release
cannot ship one that quietly resolves to "grant nothing". It also refuses a wildcard directly
over a public suffix (`*.com`, `*.co.uk`): a ceiling has to name what the business reaches.

### 3. `capsuleSandboxScopes(capsule, runtimeWriteScope, anchorSandbox)`

Signature gains a third argument. Returns the same shape with a real network block:

```js
{
  allowWrite: [...],                       // unchanged
  allowRead: [...],                        // workspace + inputs + anchor-contained externals
  network: {
    allowedDomains: capsule.network?.allowedDomains ?? [],
    deniedDomains: [],
    allowLocalBinding: capsule.network?.allowLocalBinding === true
  }
}
```

`runtime.ts` replaces the hardcoded literal at line 235 with `capsuleRun.scopes.network`.

**Corrected during implementation.** This section originally put the tunnel on a second local
port. It is on the provider's existing port instead: the sandbox routes *all* non-loopback
traffic to `httpProxyPort`, so moving that port away from the provider would have broken the
model path's own loopback allowance. The model endpoint's rules are still untouched — it
answers nothing but `POST /v1/messages*` — but its CONNECT handler, previously an
unconditional 403, now delegates to `attachEgress` with this run's admitted hosts. With no
grant the refusal is byte-identical to before. Each attempt appends one `egress_request`
event (`host`, `port`, `allowed`, `reason`, `bytes`) to the run record.

Two rules the plan did not anticipate, both in `egress.mjs`: a remote host is reachable on
80/443 only, while a granted **local** service is reachable on the port it listens on (that
grant exists so a run can drive a dev server, which never sits on 443); and a public hostname
that resolves onto a loopback or RFC1918 address is refused *after* resolution, because the
ceiling grants a name, not whatever that name points at today.

### 4. Ticket requirement block

`TicketPlanTicket` gains one optional field:

```ts
requires?: {
  /** The route that must produce the artifacts; acceptance refuses another. */
  route?: string;
  /** Declaration facts the capsule must carry before any attempt is launched. */
  capsule?: { network?: string[]; read?: string[]; tools?: string[] };
  /** Receipt keys the checker evidence must carry (see 5). */
  receipts?: string[];
}
```

### 5. Checker evidence contract

`evaluateEvidence` additionally requires, when `requires.receipts` is present, that the
evidence JSON carry a `receipts` object with those keys and that each value be a measurement,
not a claim: a non-empty list of navigated URLs, a screenshot path inside the checker
workspace whose file is non-empty, an HTTP status. A missing or empty receipt fails the check
with `receipt_missing: <key>` and is **not** behavioral — it routes to the capsule gate below,
because a receipt a worker could not produce is a scope problem, not a quality problem.

### 6. New failure classification

`FailureClassification` gains `'capsule_insufficient'`. It is produced by:

- the precondition gate, before launch, when `requires.capsule` is not satisfied by the parsed
  capsule;
- `classifyWorkerOutcome`, when the run record carries a boundary refusal
  (`egress_request` with `allowed:false`, an ASRT denial, `capsule_read_widens_*`);
- `evaluateEvidence`, on `receipt_missing`;
- acceptance, when the record's model route differs from `requires.route`.

Its reason string always names the field to change, e.g.
`capsule_insufficient: ticket requires network access to www.rangerpainting.com; capsule astra-visualizer-qa declares no network block`.

A ticket blocked as `capsule_insufficient` does **not** return to `ready` on a retry. The one
exception to `definition_changed` (line 1186) is inverted for this state: the ticket re-admits
only when `capsuleSha` changed. Editing the task to describe a workaround, re-running the same
capsule, or changing the checker leaves it blocked. Fixing the capsule is the only way forward.

## Dependency and distribution decisions

No new dependency. `@anthropic-ai/sandbox-runtime@0.0.75` already carries the allowlist and the
proxy; the egress proxy is ~60 lines of `node:http` beside `provider.ts`, matching its refusal
shape. Playwright is not a runtime dependency — it stays in the QA project and is reached
through an `allowRead` grant.

Distribution follows the `control/runtime/product-skills` precedent: this directory holds the
patch against the source tree, the tests, and the provenance. Applying it needs the runtime
rebuilt (`npm run build`) and installed, and the Anchor change needs a release publication with
a new digest. **Until that happens nothing here is enforced and no capsule can declare egress.**
Staged code is not shipped code.

## Failure map

| Path | Behaviour | Who sees it |
| --- | --- | --- |
| Capsule asks for a domain outside the Anchor | Admission refuses before launch; no run starts | `capsule_network_widens_anchor` in the admission event and the delegate result |
| Anchor has no `sandbox` block (old release) | Every egress capsule refused; existing capsules unaffected | `capsule_network_unavailable_in_release` |
| Egress proxy receives a non-admitted host | `403`, connection closed, one `egress_request` event with `allowed:false` | Run record; harness classifies `capsule_insufficient` |
| Target host down or TLS fails | Tunnel opens, transfer fails; the worker's own error surfaces | Worker output; classified behavioral, repairable |
| Worker writes a report it did not measure | Receipt check fails | `receipt_missing: <key>`, ticket blocked `capsule_insufficient` |
| Parent runs the work itself | Record's route ≠ `requires.route`; acceptance refuses | `capsule_insufficient: produced by <route>, ticket requires <route>` |
| Half-applied release (code in, Anchor out) | Declaration refused, nothing runs | `capsule_network_unavailable_in_release` |
| Read grant to a path with credentials | Not prevented by this change; the Anchor's `readableRoots` is the control | Release review at publication time |

Every one of these is visible in the run record or the delegate result. None is silent.

## Deferred

- **Egress recording of response bodies.** The proxy records host, verdict and byte count,
  not content. Body capture is a privacy decision that belongs to the owner, not to this change.
- **A general capability catalogue.** `requires` covers route, capsule facts and receipts.
  Richer capability declarations wait for a second real user.
- **The Linux isolation path.** `isolation.configuration(config)` post-processes the sandbox
  config on Linux; this deliverable is verified on macOS only and must not claim Linux
  enforcement without its own measurement.
- **Re-running the original browser QA.** It stays blocked until the release ships; the
  visualizer defect report waits on it rather than being replaced with a substitute.
