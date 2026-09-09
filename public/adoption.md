# Adopting the methods

Each guide is usable on its own: open the one that matches your current problem, supply its
concrete input (a recurring error, a confusing first task, a failed CI job, a preview gap, a
missing operation), and keep the rest unread until it applies. The four portable skills are
optional packaging for the same ideas — you can adopt one directory, fold its method into a
skill you already maintain, or simply follow the guide without installing anything.

The order below is an implementation recommendation, not a claim about your project.

| Observed situation | Smallest useful improvement | Completion evidence |
|---|---|---|
| The same rejected import or code pattern recurs | An existing lint rule with a project-specific message | It rejects the bad example and permits the valid alternative |
| Agents claim a feature works without exercising the outcome | One critical journey test with independent participants where needed | The recipient or operator sees the expected result |
| Every agent rediscovers setup or a preview URL | A reproducible bootstrap and revision-to-preview record | A fresh workspace reaches the first working result |
| You repeatedly copy CI errors into prompts | A supported command to retrieve run identity, failed logs and artifacts | The agent diagnoses the failure from that evidence |
| The same project decision must be explained repeatedly | Put it in a comment, check, test or root instruction according to scope | The next relevant task makes the intended decision |
| An agent repeatedly cannot deliver a file or inspect a result | A narrow adapter around an existing authorized transport | The actual agent route returns the expected result and useful failures |
| New people ask the same question | Improve the command, error, example or documentation they encountered | A new attempt gets past the original obstacle |
| UI and API shapes drift | Derive or generate a shared public contract | An incompatible change fails at the consumer and valid behavior still works |

## Installing a skill

An agent-skills-compatible runtime (for example Claude Code, or any harness that reads
`SKILL.md` frontmatter) picks a skill up from its skills directory. To install at the user
level on a Unix machine:

```sh
git clone https://github.com/desland01/agent-engineering-handbook
mkdir -p ~/.agents/skills
cp -r agent-engineering-handbook/skills/agent-feedback-engineering ~/.agents/skills/
```

Each skill directory is self-contained: `SKILL.md`, two reference files, and
`agents/openai.yaml` interface metadata for runtimes that display a name, short
description and default prompt. There are no other dependencies; no build step, and no
network access after installation.

Replace `agent-feedback-engineering` with whichever skill you want. You normally want one
skill for the failure you actually have — the skills overlap deliberately and you should
not load all four for every task.

## Combining a skill into one you already maintain

If you already maintain a skill that covers part of this ground, adding a whole new
directory is usually the wrong move. The smaller change is to add the relevant method as a
conditional reference inside the existing skill, with an explicit load condition, and link
to this handbook's guide. Pick the carrier by constraint:

- A standing preference or convention → a line in the skill body or the project's root
  instruction file.
- A mechanical pattern that must not recur → an executable check (lint rule, type, CI step,
  test), not prose. See [guide 01](guides/01-recurring-failures.md) and
  [guide 05](guides/05-knowledge-and-instructions.md) for choosing.
- A worked procedure with source evidence → a `references/` file loaded only when the
  trigger matches, keeping the main body short.

Keep each skill to one coherent purpose; a common word such as "accuracy" or "testing" is
not a trigger. If an existing skill already covers the ground, extend it rather than
adding a second mechanism that can drift from the first.

## A first exercise

The bundled [lint example](examples/recurring-rule/README.md) is the smallest end-to-end
demonstration of the core move: prove the unwanted import passes without the restriction,
then prove the restriction rejects it while valid imports still work. Run it with
`npm ci --ignore-scripts && npm run demo`. It is a static linting demonstration only —
it does not change any application and is not a security boundary.

## Keep human judgment where it already lives

Theo recommends writing your own `CLAUDE.md` / `AGENTS.md` rather than letting the agent
accumulate it unreviewed, at [12:29](https://www.youtube.com/watch?v=xmGY276gEFY&t=749s).
The same principle applies to skills: you retain project decisions; agents make
evidence-supported edits within the authorization you gave them. That is a division of
labor, not a prohibition on agent-assisted writing.

Claims this handbook does not make: the sponsor's price and speed claims, claims that
non-engineers become equally effective, universal career outcomes, and the permanent
elimination of whole error classes are treated as unverified marketing or qualified
opinion. See [validation.md](validation.md) for exactly what was run.
