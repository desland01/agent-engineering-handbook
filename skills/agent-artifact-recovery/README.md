# Artifact recovery

This skill helps an agent resume interrupted work without repeating stages that already finished. You can inspect its reconciliation to see what remains and whether recovery duplicated any effects.

## Use it when work stops midway

Reach for this skill after a pipeline crashes while some outputs or delivery steps have already completed. It also helps when a corrected result looks stale because an older artifact reached the destination. Use it when productive work succeeded, yet the required structured summary was lost or malformed. Choose output verification when you only need to judge a completed result against its original request. Choose another skill when the problem concerns recurring guidance, missing tools, workspace setup, or contract consistency.

## Give it records and real artifacts

Supply every artifact left by the interrupted or suspect run, including outputs that appear complete. Include the original work order, available receipts, and the pipeline stages that could have run. Provide delivery evidence separately because production, transport, and receipt records can describe different states. For summary recovery, provide the recorded session identity and persisted outputs such as commits or uploaded files. If the session identity is missing, the agent reports that limit before proposing an authorized restart.

## The agent compares intention with reality

The work order identifies what should happen before processing begins and where the result belongs. The finished artifact receives a fingerprint from its actual bytes only after production finishes. The agent compares that fingerprint before reusing an existing artifact or copying it toward delivery. A different fingerprint proves different bytes, while correctness still requires checks against requested inputs and outcomes. The agent preserves an uncertain artifact when evidence cannot show whether rebuilding or resending is necessary.

## Measured properties decide whether work survived

The agent checks a property that reveals completeness, such as duration, row counts, or required sections. You choose each property, tolerance, and overrun policy from the requested output and your product's evidence. An unreadable measurement prevents reuse, while a product's declared policy decides how acceptable overruns are handled. The agent validates recorded size before trusting a receipt, then re-derives information from invalid receipts. Outside changes can preserve size while changing bytes, so possible outside edits require a fresh fingerprint.

## Recovery resumes only the missing stage

Before mutation begins, the agent snapshots the previous receipt and current listing into a stable starting point. It decides reusable artifacts once the complete batch is known, avoiding decisions from changing pipeline state. Missing receipts produce a smaller reuse plan, while verified existing artifacts proceed through their remaining delivery step. A refused reuse batch falls back to delivering verified artifacts already held by the machine. Persisted work supports this approach, as Dexter Horthy says <a href="#cite-c0089">you can always resume from where you left off</a>. When only the summary failed, the agent resumes that recorded session to extract the result instead. It compares persisted outputs before and after extraction because instructions alone cannot guarantee read-only behavior.

## Its report makes each decision visible

The result separates what was produced, what delivery evidence proves, and what each receipt records. Reused items include the actual-byte comparison that justified reuse and the completeness check they passed. Reworked items state why production must happen again instead of repeating only a missing delivery step. Summary recovery includes the extracted result plus evidence that persisted outputs stayed unchanged during extraction. The included trial cases describe these checks, although those cases remain designed and have never run.

## The limits prevent unsafe recovery

A fingerprint difference cannot identify the correct version, so the agent also checks requested properties and outcomes. Product-specific measurements cannot be copied safely from another pipeline without evidence from your own output. Cached receipts can become stale after outside changes, especially when replacement bytes keep the same size. The source evidence came from one setup, so repeatability must be measured under your production conditions. The skill does not authorize credentials or external effects beyond the original session's allowed scope. Use a standing check after recovery when the same interruption pattern keeps returning.

## Selected evidence supports resumable work

The selected source contributes one qualified example of preserving work so a later run can resume. That example supports durable progress records, while the skill body supplies recovery decisions and safeguards. The source does not prove this package works, and the included evaluation cases remain unexecuted.

<ol id="citations"><li id="cite-c0089">Dexter Horthy, video, <a href="https://www.youtube.com/watch?v=YwZR6tc7qYg&t=1586s">From RPI to QRSPI - Lessons Learned Rolling out Research/Plan/Implement to thousands of engineers</a>, at 26:26. "you can always resume from where you left off"</li></ol>

<p id="next-action">Assemble one recovery packet containing an interrupted run's artifacts, work order, receipts, delivery evidence, and session record.</p>
