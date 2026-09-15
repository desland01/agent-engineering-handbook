# Output verification

A success message can hide missing work, skipped stages, or an unusable result. You can use this skill to make an agent define completion, inspect the output, and report only supported conclusions.

## Use it when success looks uncertain

Reach for this skill when one agent run reports success, yet its deliverable may remain incomplete. It suits builds, generated documents, exports, and transformations with a concrete result to accept. Choose another method for recurring rules, interrupted recovery, workspace setup, or complete user-journey testing.

## Give it the acceptance basis

You supply the requested change, the produced result, and access needed to inspect that result. Also provide the process that produced it and any recorded expectations or earlier versions. The agent derives required properties from your request instead of copying assumptions from old output.

## The agent checks completion in layers

First, it confirms the promised result exists where its intended consumer can reach it. Next, it checks every required stage for omissions, placeholders, substitutions, or misleading completion reports. Finally, it exercises properties the requester cares about, such as opening, playing, rendering, or feeding later work. Theo Browne describes checking that a sent message appears and renders for its recipient <a href="#cite-c0002">in his video</a>. Existing checks remain usable only when they cover the result and that result has not changed.

## Bad cases show whether checks work

For each believable false success, the agent chooses the smallest check that would expose it. It then rejects a deliberately damaged disposable example while allowing an equivalent healthy example through. A useful failure names the broken property, while a useful pass names exactly what was measured. The packaged trial scenarios remain unrun, so they currently demonstrate coverage plans rather than measured improvement.

## The verdict keeps its limits visible

The final verdict lists checked properties, rejected false-success paths, and anything still unverified in this environment. Verification depth follows the consequence, so a simple report may need fewer checks than shipped software. A passing check supports only its measured property, never every quality someone might infer. This skill judges one run and leaves interrupted recovery or permanent safeguards to other methods.

## The sources support outcome-based verification

The selected evidence supports checking meaningful outcomes instead of trusting a task's success signal alone. Alex, Erik Schluntz, and Barry Zhang recommend adding tests for outcomes that truly matter <a href="#cite-c0116">during their discussion</a>. These sources support targeted verification, while the skill's broader sequence comes from its inspected implementation examples.

<ol id="citations"><li id="cite-c0002">Theo Browne, video, <a href="https://www.youtube.com/watch?v=xmGY276gEFY&t=254s">A Message for Passionate Devs</a>, at 04:14. "make sure it actually appears and renders properly"</li><li id="cite-c0116">Alex, Erik Schluntz, Barry Zhang, video, <a href="https://www.youtube.com/watch?v=LP5OCa20Zpg&t=751s">Building effective agents</a>, at 12:31. "add tests for the things that you really care about"</li></ol>

<p id="next-action">Write three request-derived acceptance properties for one recently completed agent run before accepting its result.</p>
