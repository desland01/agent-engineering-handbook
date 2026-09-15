# You keep shared contracts consistent across layers

You can keep one domain object consistent from storage through every interface that consumes it. You will trace its authoritative contract, derive each consumer, and check types, runtime data, permissions, and compatibility separately.

## One contract gives every layer one meaning

Choose one domain object, then trace its meaning through storage, services, transports, and every consuming interface. Record its accepted name, public fields, allowed states, and durable decisions in one authoritative definition. <a href="#cite-c0247">Matt Pocock directs attention to module interfaces</a>, because those seams determine how changes travel between layers. <a href="#cite-c0408">An early smol-ai workflow added a shared dependency plan</a> before generating separate files, keeping their assumptions aligned.

## Derived consumers remove competing shapes

Make each consumer derive its request, response, and error shapes from that authoritative public contract. Keep storage details behind the boundary so public consumers receive only fields their work requires. Route local and remote callers through one supported transport, preventing a quiet second contract from forming. Typed errors should distinguish actions such as retrying, updating, requesting access, or stopping safely. <a href="#cite-c0525">Ryan Lopopolo describes typed interfaces and boundary validation</a> that prevent agents from inventing unsupported data shapes.

## Types catch drift before execution

Change one shared field deliberately, then run the existing type check against every derived consumer. A useful failure names the stale consumer, while the corrected contract allows the legitimate path. <a href="#cite-c0541">逆瀬川ちゃん recommends turning architecture decisions into executable checks</a>, so written boundaries cannot quietly decay. Keep those checks close to the shared boundary, where one failure can expose cross-layer drift. A dependency rule proves only the imports it examines, without creating an execution sandbox.

## Runtime checks cover what types cannot

A type check compares declared shapes before execution, while incoming values can still violate those declarations. Validate untrusted values at the real boundary before your application stores, transforms, or returns them. Check authorization separately, because a well-formed request may still belong to an unauthorized caller. Treat machine suitability as an operating condition, never as proof that an untrusted process lacks access. <a href="#cite-c0428">Armin Ronacher argues for making malformed cases impossible to write</a>, reducing later defensive patches.

## Deployed clients still need compatibility

Shared definitions coordinate code that receives them, but they cannot update clients already running elsewhere. Use additive changes, explicit versions, or a compatibility window whenever consumers deploy on different schedules. Test one stale consumer against the changed boundary, then confirm its failure is deliberate and understandable. A compatible response preserves accepted behavior, while an incompatible change produces a typed, actionable refusal.

## One trace proves the contract holds

Choose one object and write its authoritative name, public shape, valid states, and error outcomes. List every producer and consumer, including storage, services, transport handlers, interfaces, and background jobs. Remove copied definitions, derive supported consumers, and keep one public transport wherever callers share behavior. Then run three checks: break a field, send malformed data, and attempt unauthorized access. Finally, exercise an older client and confirm compatibility behavior matches the decision you recorded. That sequence tests each guarantee at its own boundary without treating one passing check as universal proof.

## The evidence supports enforced shared boundaries

The sources show that interfaces become safer when their contracts are shared, derived, and mechanically checked. They cover generated files, module seams, malformed states, typed boundaries, and executable architecture rules. They do not prove one library, transport, or type system works for every application. They also leave runtime permissions and deployed-client compatibility as separate engineering responsibilities.

<ol id="citations"><li id="cite-c0247">Matt Pocock, video, <a href="https://www.youtube.com/watch?v=nQwJVHCtDDY&amp;t=155s">Building AI Coding Agents with Matt Pocock</a>, at 02:35. "thinking about the interfaces between all of the modules in your codebase"</li><li id="cite-c0408">smol-ai (Shawn "swyx" Wang), repo, <a href="https://github.com/smol-ai/developer#:~:text=asking%20GPT%20to%20think%20through%20shared_dependencies.md%20%2C%20and%20then%20insisting%20on%20using%20that">smol-ai/developer</a>, at We solved this by adding an intermediate step. "asking GPT to think through shared_dependencies.md , and then insisting on using that"</li><li id="cite-c0428">Armin Ronacher, blog, <a href="https://lucumr.pocoo.org/2026/6/23/the-coming-loop/#:~:text=make%20the%20malformed%20case%20unrepresentable%20or%20impossible%20to%20write">The Coming Loop</a>, at Furthermore it's well understood that models tend to. "make the malformed case unrepresentable or impossible to write"</li><li id="cite-c0525">Ryan Lopopolo, blog post, <a href="https://openai.com/index/harness-engineering/#:~:text=we%20validate%20boundaries%20or%20rely%20on%20typed%20SDKs">Harness engineering: leveraging Codex in an agent-first world</a>, at Instead, we started encoding what we call “golden. "we validate boundaries or rely on typed SDKs so the agent can't accidentally build"</li><li id="cite-c0541">逆瀬川ちゃん, blog post, <a href="https://nyosegawa.com/en/posts/harness-engineering-best-practices-2026/#couple-adrs-with-executable-rules">Harness Engineering Best Practices for Claude Code / Codex Users, Explained Plainly</a>, at Couple ADRs with executable rules. "encoding the architecture decision as an executable check."</li></ol>

<p id="next-action">Trace one domain object today and verify its contract at every producer, boundary, and consumer.</p>
