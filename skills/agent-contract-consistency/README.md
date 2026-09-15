# Contract consistency

This skill makes an agent reconcile one shared interface across storage, services, clients, and visible behavior. You can then check that changes fail safely and valid requests still complete through the real connection.

## Contract drift appears across repeated shapes

Reach for this skill when one business object has conflicting names, fields, routes, or errors across layers. It also fits a planned rename, added field, or changed error that existing consumers must follow. Use another method when the interface lacks the needed operation, knowledge, workspace, or recurring-rule mechanism. New interface design also falls outside this skill because no existing contract needs reconciliation.

## Your project supplies the authority

You provide the interface, every known consumer, the proposed change or observed mismatch, and existing project language. The agent reads durable decisions before naming anything, because accepted terms can encode deliberate relationships. It identifies the current authoritative definition, then derives consumers from that source instead of preserving copied versions. An external schema or server response may supply that authority, depending on your existing system.

## One contract guides every consumer

The agent traces one object from storage through transformations, responses, callers, and the interface people use. It removes competing definitions and keeps private storage details outside the public response when required. It validates untrusted inputs where they enter, using the system's actual rules for accepted data. Known errors receive stable names linked to distinct actions, while unfamiliar failures remain available for diagnosis. <a href="#cite-c0247">Matt Pocock emphasizes thinking about interfaces between all modules in a codebase.</a>

## Negative checks expose hidden mismatches

You see this skill working when a deliberate rename makes every derived consumer fail before release. Invalid external data should fail at runtime through the same boundary that receives real requests. A renamed error should expose stale handlers instead of quietly sending every failure toward one fallback. The unchanged control must still pass end to end through the actual client and server connection. Authorization needs its own refused request, checked at the server boundary rather than inferred from agreement.

## The result states remaining gaps

The finished work includes one reconciled contract, removed duplicates, boundary validation, and mapped error actions. It also states which deployed clients, permissions, or unchecked dependencies remain outside those guarantees. You can review the evidence beside each change instead of accepting consistency from inspection alone.

## Separate guarantees keep conclusions honest

Shared types constrain accepted code, while runtime checks constrain the data that actually arrives. Neither proves permission, so the agent checks authorization separately where the server receives requests. Older deployed clients remain unchanged, requiring additive changes or an explicit compatibility policy. Corrupt optional reuse records may degrade safely, while required authoritative data must surface an error. Static dependency rules cover only listed imports, and environment markers only describe machine suitability. The supplied evaluation cases remain designed examples, so they provide no measured effectiveness result.

## Sources show interfaces need deliberate boundaries

One recorded talk supports careful attention to interfaces between modules in a codebase. The skill's detailed procedure comes from inspected project examples that were not executed for this edition. That evidence supports the practice without establishing universal results, automatic authorization, or deployed-client compatibility.

<ol id="citations"><li id="cite-c0247">Matt Pocock, video, <a href="https://www.youtube.com/watch?v=nQwJVHCtDDY&t=155s">Building AI Coding Agents with Matt Pocock</a>, at 02:35. "thinking about the interfaces between all of the modules in your codebase"</li></ol>

<p id="next-action">Give the agent one changed interface and ask it to prove every consumer still agrees.</p>
