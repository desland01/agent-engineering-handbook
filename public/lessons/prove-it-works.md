# You test the result users actually need

A green check can still leave the user's actual result broken and unusable. You will define one accepted result and test it through the user's real journey. You will also prove that the final gate rejects a false success.

## Accepted results define useful success

Write one sentence naming the producer, the receiver, and the observable result they must receive. Add the properties that distinguish a finished result from an artifact that merely exists. A completed command proves only that its selected work ran without a reported failure. Hamel Husain and Shreya Shankar recommend evaluating actual outcomes instead of technical implementation alone <a href="#cite-c0402">in their evaluation guide</a>. Harrison Chase warns that an error-free agent can still perform terribly for users <a href="#cite-c0493">in his monitoring analysis</a>.

## User journeys expose hidden failures

Place the decisive assertion where the user encounters the result, after every required handoff. In Theo Browne's example, one participant sent a message and another checked its rendered appearance <a href="#cite-c0002">in the receiving interface</a>. That boundary tested delivery between participants instead of trusting the sender's successful action. Use separate participants only when independence belongs to the outcome you need to protect. This pattern is one example, and your own accepted result should determine the journey.

## Focused checks protect important outcomes

Choose checks for outcomes whose failure would cost trust, money, or completed work. Alex, Erik Schluntz, and Barry Zhang recommend adding tests for the things you truly care about <a href="#cite-c0116">in their agent-building discussion</a>. That principle supports a small decisive test before broad coverage that answers weaker questions. Add another kind of check only when it detects a remaining false-success path. Stop adding checks when the accepted result is adequately proved by the evidence already gathered. Record each unsupported case so later reports preserve the boundary of your evidence.

## Different properties need different evidence

A distributed package may pass source tests while failing when its intended consumer installs it. A supported minimum runtime may break even when the newest environment remains green. A compiler check can reject invalid generated output before users depend on it. A final artifact may look correct while its source report still contains unfinished parts. Each check answers one property, so no single passing layer proves the entire result. These are examples, and your accepted result determines which layers you need.

## Reproduction turns surprises into tests

Save the starting seed, relevant options, software revision, and environment when an unexpected case appears. A seed lets the same generated input appear again, making the failure repeatable. Remove unrelated details until the smaller case still produces the same failure. Add that smallest useful case to your tests while keeping the original reproduction record. The original record preserves environmental details that may disappear during later reduction. When a similar case stays outside current scope, tie the exception to its exact reproduction.

## Baselines keep changes meaningful

A baseline records expected behavior, including known limitations that remain accepted for now. Classify every difference as an improvement, regression, intended change, or unresolved discrepancy before updating expectations. Update the baseline only after you understand the behavior and have authority to accept it. Preserve the previous result and reason in normal change history for later investigation.

## Benchmarks compare equivalent work

Use the same inputs, options, machine, and runtime before comparing performance results. Separate warm-up runs from repeated measurements before directly comparing the recorded results. Keep the raw timings beside a robust summary that resists one unusual result. Confirm that every faster result still produces the accepted output before claiming improvement. When ordinary variation resembles the measured gain, report uncertainty instead of selecting the fastest run. Comparable evidence matters more than a dramatic number produced under different conditions.

## Final gates must reject bad results

Trace the check people trust until you reach the exact result controlling release or delivery. A reassuring job name may hide omitted child checks, skipped work, or the wrong environment. Make the real gate reject a disposable case containing the relevant bad result. Run the same gate on the intended result and confirm it accepts that result. Michael Truell, Kevin Niparko, and Tomas Reimers describe verification through testing software and clicking its buttons <a href="#cite-c0288">in their keynote</a>. Ryan Lopopolo reports using browser tooling to reproduce bugs and validate fixes through user-facing behavior <a href="#cite-c0522">in his harness account</a>. Interface checks answer behavior questions, while compiler checks answer whether generated output remains valid. Your report should name each executed layer because every passing check has a limited boundary.

## The sources show outcome-focused verification

Together, these sources distinguish successful execution from results that actually work for users. The videos support targeted journey checks and direct interaction with the finished interface. The articles support outcome evaluation, quality checks beyond error counts, and browser-based validation of fixes. They do not establish one required testing stack for every product or change.

<ol id="citations">
<li id="cite-c0002">Theo Browne, video, <a href="https://www.youtube.com/watch?v=xmGY276gEFY&t=254s">A Message for Passionate Devs</a>, at 04:14. "make sure it actually appears and renders properly"</li>
<li id="cite-c0116">Alex, Erik Schluntz, Barry Zhang, video, <a href="https://www.youtube.com/watch?v=LP5OCa20Zpg&t=751s">Building effective agents</a>, at 12:31. "add tests for the things that you really care about"</li>
<li id="cite-c0288">Michael Truell, Kevin Niparko, Tomas Reimers, video, <a href="https://www.youtube.com/watch?v=fWa7uxyhVDE&t=1498s">Cursor Keynote | Compile 26</a>, at 24:58. "actually testing the software and clicking through buttons"</li>
<li id="cite-c0402">Hamel Husain, Shreya Shankar, blog, <a href="https://hamel.dev/blog/posts/evals-faq/#:~:text=evaluate%20actual%20outcomes%20rather%20than%20technical%20implementation">AI Evals: Everything You Need to Know</a>, at As time goes on you should lean towards. "evaluate actual outcomes rather than technical implementation."</li>
<li id="cite-c0493">Harrison Chase, blog, <a href="https://blog.langchain.dev/in-software-the-code-documents-the-app-in-ai-the-traces-do/#monitoring-shifts-from-uptime-to-quality">In software, the code documents the app. In AI, the traces do.</a>, at Monitoring Shifts from Uptime to Quality. "An agent can be "up" with 0 errors and still be performing terribly"</li>
<li id="cite-c0522">Ryan Lopopolo, blog post, <a href="https://openai.com/index/harness-engineering/#:~:text=reproduce%20bugs%2C%20validate%20fixes%2C%20and%20reason%20about%20UI%20behavior%20directly">Harness engineering: leveraging Codex in an agent-first world</a>, at For example, we made the app bootable per. "reproduce bugs, validate fixes, and reason about UI behavior directly."</li>
</ol>

<p id="next-action">Write one accepted-result sentence for the user journey whose failure would cause the greatest harm.</p>
