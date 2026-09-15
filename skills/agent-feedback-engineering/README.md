# Feedback engineering

When an agent repeats a mistake, this skill turns the observed failure into a reusable check. You supply the failure evidence, and the agent selects the carrier that fits its constraint. You can then verify the bad case is blocked while valid work still passes.

## Recurring failures justify a standing check

Reach for this skill when an agent repeats a mistake across runs or you request a lasting guard. It also applies when review feedback should become automation instead of another manual correction. Boris Cherny describes automating recurring review comments with a lint rule <a href="#cite-c0187">in his recorded explanation</a>. Use bug diagnosis for a single unexplained failure, and use architecture guidance for general refactoring.

## Evidence defines the check's boundary

Give the skill the observed failure, evidence showing it, and the project where the check belongs. A concrete bad case lets the agent identify the exact property that needs protection. The agent pairs that failure with a known-good case so proof covers both boundaries. Recurrence normally justifies the guard, while your explicit request can justify one after a single defect.

## Existing rules receive the constraint first

The agent first searches for an existing rule that already reaches the failure's boundary. It extends that mechanism when possible, avoiding a second check that could drift later. Possible carriers include compiler checks, pattern checks, behavior tests, shared gates, project guidance, and reusable skills.

## The failure chooses the mechanism

Invalid data shapes belong in compiler checks, while repeated code patterns belong in file-wide pattern checks. Runtime mistakes need tests that assert the specific symptom, rather than merely confirming nothing crashed. Repository-wide conditions belong at a shared gate, while judgment calls belong in guidance the agent reads. Guidance steers decisions, so written words alone never prove the failure has become impossible.

## Proportionate proof shows the change working

For an executable check, the agent first demonstrates that the recorded bad case currently passes. After the smallest correction, that case must fail while a known-good case still passes. The agent also confirms the real project command loads the check strongly enough to stop the run. Instruction changes receive a wording review and a loading inspection when delivery could vary. Each finished change records what the rule enforces, why it exists, and where it lives.

## Exceptions remain explicit and narrow

Legitimate exceptions belong in narrow allowances or targeted suppressions instead of weakening the entire check. When correct work triggers the rule, the agent narrows the pattern or records a justified exception. Broad escapes that silence errors without changing behavior do not count as successful proof. The skill cannot prove coverage beyond the tested boundary or prevent every future variation.

## The sources support repeated-failure guards

These sources show practitioners moving repeated failures from human review into durable project checks. Cherny's example supports choosing a narrow automated rule for repeated review comments <a href="#cite-c0187">in his interview</a>. Theo Browne describes automating a recurring issue class <a href="#cite-c0005">in his discussion of feedback engineering</a>. Neither statement proves that one check will catch every future form of a failure.

<ol id="citations"><li id="cite-c0187">Boris Cherny, video, <a href="https://www.youtube.com/watch?v=julbw1JuAz0&t=2495s">Inside Claude Code with Boris Cherny</a>, at 41:35. "I would write a lint rule for it. So just automate it"</li><li id="cite-c0005">Theo Browne, video, <a href="https://www.youtube.com/watch?v=xmGY276gEFY&t=495s">A Message for Passionate Devs</a>, at 08:15. "that class of issue can be fully automated forever."</li></ol>

<p id="next-action">Bring one repeated agent mistake and its clearest failure evidence to a feedback-engineering run.</p>
