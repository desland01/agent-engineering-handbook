# You turn repeated mistakes into reliable checks

When the same mistake returns, turn the correction into a check that runs on each change. You will learn to choose its boundary and prove that it rejects the mistake while allowing valid work.

## Observed failures define useful checks

Begin with work that already failed, because imagined dangers create noisy and expensive rules. Keep one failing example and one valid alternative before deciding how any check should behave. Hamel Husain and Shreya Shankar recommend building evaluators from discovered errors in <a href="#cite-c0400">their guidance</a>. A recurrence usually justifies automation, while one severe failure can justify earlier protection. An explicit request for a standing guard also removes the need to wait.

## Repeated comments should become executable rules

Repeated review comments show that memory and written guidance are no longer reliable controls. Boris Cherny says he would write a lint rule and automate that repeated feedback in <a href="#cite-c0187">his recommendation</a>. Ryan Lopopolo describes promoting a missed written rule into code when documentation falls short in <a href="#cite-c0519">the described practice</a>. Choose the smallest existing mechanism that recognizes the entire demonstrated class of mistakes. Use a static rule when the failure has a visible and stable code shape. Use a focused test when the failure appears only while the software runs.

## The check must permit valid work

A useful check protects one boundary without rejecting every nearby and acceptable change. Save the forbidden example, then preserve one approved alternative beside it for comparison. Set the rule to block changes when both the boundary and remedy are certain. Use a warning while evidence remains incomplete, then remove or strengthen that warning. Narrow exceptions should name their reason, because broad escape routes hide future recurrences. Theo Browne says an entire recurring issue class can be automated permanently in <a href="#cite-c0005">his argument</a>. That promise applies only inside the precise boundary the chosen mechanism can observe.

## A small import rule proves the boundary

Suppose interface code repeatedly imports a database client instead of using the approved service layer. The following exercise creates one forbidden import, one permitted import, and one blocking rule. Type these commands inside an empty working directory on a development machine.

```sh
mkdir recurring-import-check
cd recurring-import-check
npm init -y >/dev/null
npm install --save-dev eslint@10.10.0
npm pkg set type=module
npm pkg set 'scripts.lint=eslint .'
mkdir -p src/db src/api src/ui

cat > src/db/client.js <<'EOF'
export const db = {};
EOF

cat > src/api/users.js <<'EOF'
import { db } from "../db/client.js";
export const users = db;
EOF

cat > src/ui/UserCard.js <<'EOF'
import { db } from "../db/client.js";
export const card = db;
EOF

cat > src/ui/UserList.js <<'EOF'
import { users } from "../api/users.js";
export const list = users;
EOF

cat > eslint.config.red.js <<'EOF'
export default [{ files: ["src/ui/**/*.js"], rules: {} }];
EOF

cat > eslint.config.js <<'EOF'
export default [
  { ignores: ["node_modules/**"] },
  {
    files: ["src/ui/**/*.js"],
    rules: {
      "no-restricted-imports": [
        "error",
        {
          patterns: [{
            group: ["**/db", "**/db/**", "@db/*"],
            message: "UI code must import through the API layer."
          }]
        }
      ]
    }
  }
];
EOF

npx eslint --config eslint.config.red.js src
npx eslint src/ui/UserList.js
set +e
npm run lint
status=$?
set -e
test "$status" -eq 1
```

The unprotected validation succeeds, proving the recurring mistake remains invisible to routine checks. The protected validation rejects the direct import, while the approved service import remains accepted. The ordinary project command uses the same protection, so future changes cannot depend on memory.

## Ordinary validation keeps protection active

A check run only by hand still depends on someone remembering when to use it. Place it inside the project's ordinary validation, using the same command locally and during shared review. Make every failure message name the approved alternative, so rejection includes the next correction. Mitchell Hashimoto describes changing the environment after failure so an agent cannot repeat that mistake in <a href="#cite-c0374">his account</a>. 逆瀬川ちゃん recommends adding a test whenever an agent makes a mistake in <a href="#cite-c0536">the stated practice</a>. Together, those practices move correction from a person's memory into the environment surrounding future work.

## Every check needs limits and upkeep

The import rule sees direct imports matching configured locations, while other dependency routes remain outside. Dynamic loading, indirect re-exports, and unchecked folders require separate evidence before receiving additional protection. Record these limits beside the rule, then expand only after observing another missed class. Review exceptions and messages whenever architecture changes, because an outdated remedy can block valid work. Retire the rule when its boundary disappears or a broader control safely replaces it. Automation reduces repeated correction, while maintenance decides whether the long-term cost remains worthwhile.

## Sources support evidence-led automation

Together, these sources support replacing repeated correction with an executable guard around an observed failure. They favor checks built from discovered errors and written rules that have already failed. They describe practitioner guidance and experience, rather than measurements proving universal outcomes. Each local check still requires direct proof that forbidden work fails and permitted work succeeds.

<ol id="citations">
<li id="cite-c0005">Theo Browne, video, <a href="https://www.youtube.com/watch?v=xmGY276gEFY&amp;t=495s">A Message for Passionate Devs</a>, at 08:15. "that class of issue can be fully automated forever."</li>
<li id="cite-c0187">Boris Cherny, video, <a href="https://www.youtube.com/watch?v=julbw1JuAz0&amp;t=2495s">Inside Claude Code with Boris Cherny</a>, at 41:35. "I would write a lint rule for it. So just automate it"</li>
<li id="cite-c0374">Mitchell Hashimoto, blog, <a href="https://mitchellh.com/writing/my-ai-adoption-journey#:~:text=engineer%20a%20solution%20such%20that%20the%20agent%20never%20makes%20that%20mistake%20again.">My AI Adoption Journey</a>, at I don't know if there is a. "engineer a solution such that the agent never makes that mistake again."</li>
<li id="cite-c0400">Hamel Husain, Shreya Shankar, blog, <a href="https://hamel.dev/blog/posts/evals-faq/#:~:text=Write%20evaluators%20for%20errors%20you%20discover%2C%20not%20errors%20you%20imagine.">AI Evals: Everything You Need to Know</a>, at A better approach is to start with error. "Write evaluators for errors you discover, not errors you imagine."</li>
<li id="cite-c0519">Ryan Lopopolo, blog post, <a href="https://openai.com/index/harness-engineering/#:~:text=When%20documentation%20falls%20short%2C%20we%20promote%20the%20rule%20into%20code">Harness engineering: leveraging Codex in an agent-first world</a>, at Human taste is fed back into the system. "When documentation falls short, we promote the rule into code"</li>
<li id="cite-c0536">逆瀬川ちゃん, blog post, <a href="https://nyosegawa.com/en/posts/harness-engineering-best-practices-2026/#:~:text=Whenever%20an%20agent%20makes%20a%20mistake%2C%20add%20a%20test%20to%20prevent%20it.">Harness Engineering Best Practices for Claude Code / Codex Users, Explained Plainly</a>, at Tests resist rot better than documentation. "Whenever an agent makes a mistake, add a test to prevent it."</li>
</ol>

<p id="next-action">Convert one recently repeated mistake into a blocking check with one permitted example.</p>
