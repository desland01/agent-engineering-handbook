# 06 — Build small tool adapters for capability gaps

Practical guide for closing a specific gap between what your agent needs to do and what its
existing tools can do. Companions: [01](01-recurring-failures.md) ·
[03](03-preview-workspaces.md) · [05](05-knowledge-and-instructions.md) ·
[07](07-team-learning.md).

Source: [Theo's video](https://www.youtube.com/watch?v=xmGY276gEFY).

## What the video and public PR show

Theo describes a gap in his agents’ GitHub media-upload workflow at
[05:56](https://www.youtube.com/watch?v=xmGY276gEFY&t=356s). His solution is a small
Cloudflare-backed file service and a file-upload skill. This is his reported gap;
verify the current tools available in your environment before building a replacement.

The [inspected 06:23 frame](../screenshots/06-23-upload-skill.jpg) shows an actual
SKILL.md with an upload trigger, a PUT request, a file body, an upload-token environment
variable and a public output URL. It does not show the server implementation or prove
that a particular upload succeeded. [Melee PR #13](https://github.com/t3dotgg/melee4mac/pull/13)
independently shows screenshot URLs on the same `files.tslop.org` host.

The implementation procedure below is an adaptation. No service was deployed or upload
performed in this task. Use [the full evidence gallery](../evidence.html) for the frames.

## When to apply

Build an adapter when all three hold:

- An agent fails at an important step for lack of a tool (not lack of knowledge — lack of
  knowledge belongs in [guide 05](05-knowledge-and-instructions.md)).
- No existing tool covers it after a real search.
- The adapter is smaller than the recurring workaround it replaces.

## Implementation

1. **Write the gap as one sentence.** "Agents cannot attach a video to a PR they created."
   Keep the intended operation precise enough to verify.
2. **Search for reuse before building.** Check the CLI and API surface first — check what your selected tools actually expose. Prefer an
   existing integration; build only the missing piece.
3. **Choose the smallest service shape.** A local wrapper may suffice. For an authorized shared uploader, reuse existing authentication and storage, expose only the needed operation, and return the result in a predictable shape.
4. **Write the skill so the agent can use it unaided**: when to use it, the exact call, the existing credential-loader name (no secret values), actual size limits, and a result example.
5. **Protect the key.** Distribute per-machine, scope it to upload-only, allow rotation, and
   never put it in the repository or the skill text.
6. **Test inside the agent.** Run the blocked operation through the actual selected agent tool route. The acceptance test is the agent
   completing the step end to end without a hint.
7. **Set a deletion plan.** A one-off service with an auth key is a liability the day the
   workflow changes. Note who owns it and when it should be retired.

## Concrete example

Illustrative skill frontmatter and body shape (written for this guide, **not executed
against any real service**; the video's service URL and key are Theo's, and none of this
describes a deployed system here):

```markdown
---
name: pr-media-upload
description: Upload a video or image so it can be linked in a PR description. Use when an
  agent must attach media evidence to a pull request and no CLI route exists.
---

Upload with: curl --fail-with-body --data-binary "@artifact.png" \
  -H "Authorization: Bearer $MEDIA_UPLOAD_KEY" \
  "https://your-authorized-host.example/upload"
The response is {"url": "..."}. Return the URL; attach it to a PR only within the requested publishing scope.
Limit: document the actual configured limit. Never upload files containing secrets.
```

## Acceptance

- An agent, given only the skill, completes the blocked step with no extra hints.
- The service rejects unauthenticated and oversized uploads, and the key rotates without
  client code changes.
- The workflow it replaces no longer needs a human.
- A runbook exists for rebuilding the service from its repository.

## Failure modes and maintenance

- **Shadow infrastructure.** One-off services outlive their purpose. Track them in a list
  with owners and review dates, like any other service.
- **Key leakage.** An upload endpoint with a widely copied key is an abuse magnet. Rate
  limit, scope to upload-only, and monitor volume.
- **Skill rot.** When a native route replaces it, migrate callers, verify results, and retire the adapter through the existing recovery process.
- **Over-building.** Reassess extra state and endpoints against the actual capability gap; endpoint count alone does not determine quality.
- **Boundary honesty.** Build-versus-reuse applies inside your authorization: this pattern
  is for capability gaps in your own workflow, evaluated on evidence, with no vendor switch
  by default and nothing adopted from a sponsor segment.
