#!/usr/bin/env bash
# Build a sandbox HOME that gives a worker a genuinely blind control arm.
#
# WHY THIS EXISTS
# Every ~/.claude-*-worker/skills is a SYMLINK to the live farm ~/.claude/skills. So once a
# skill is installed, any worker auto-loads it and a "control" arm silently stops being one.
# guardrails.mjs refuses to move a skill out of the farm mid-session, so you cannot
# un-install one to recover a control.
#
# grok-worker derives BOTH its config dir and its proxy token from $HOME:
#     CFG="$HOME/.claude-grok-worker"
#     TOKFILE="$HOME/.cli-proxy-api/local-token"
# so overriding HOME swaps the whole surface in one move.
#
# No secret is ever copied to a wider-readable place: the proxy token is SYMLINKED, so its
# own file permissions still apply. .claude.json is copied with -p to preserve mode 600, and
# lands inside the owner's home, never /tmp.
#
# Usage:
#     build_blind_sandbox.sh <skill-to-exclude>
#     HOME=~/.sandbox-eval-home        grok-worker ...   # blind control
#     HOME=~/.sandbox-eval-home-with   grok-worker ...   # treatment
#
# Delete both when finished; this script rebuilds them in seconds.
set -euo pipefail

SKILL="${1:?usage: build_blind_sandbox.sh <skill-name-to-exclude>}"
FARM="$HOME/.claude/skills"
REAL="$HOME/.claude-grok-worker"
WITHOUT="$HOME/.sandbox-eval-home"
WITH="$HOME/.sandbox-eval-home-with"

[[ -d "$FARM/$SKILL" ]] || { echo "no such skill: $FARM/$SKILL" >&2; exit 2; }

for target in "$WITHOUT" "$WITH"; do
  case "$target" in "$HOME"/.sandbox-eval-home*) ;; *) echo "refusing: $target" >&2; exit 1;; esac
  rm -rf "$target"
  mkdir -p "$target/.cli-proxy-api" "$target/.claude-grok-worker/skills"
  ln -s "$HOME/.cli-proxy-api/local-token" "$target/.cli-proxy-api/local-token"
  for f in .claude.json settings.json CLAUDE.md; do
    [[ -e "$REAL/$f" ]] && cp -p "$REAL/$f" "$target/.claude-grok-worker/$f"
  done
  for d in agents commands hooks output-styles rules-on-demand plugins; do
    [[ -e "$REAL/$d" ]] && ln -s "$(readlink "$REAL/$d" 2>/dev/null || echo "$REAL/$d")" \
      "$target/.claude-grok-worker/$d"
  done
  for s in "$FARM"/*; do
    name="$(basename "$s")"
    [[ "$name" == "$SKILL" && "$target" == "$WITHOUT" ]] && continue
    ln -s "$s" "$target/.claude-grok-worker/skills/$name"
  done
done

echo "without: $(ls "$WITHOUT/.claude-grok-worker/skills" | wc -l | tr -d ' ') skills, $SKILL present: $([[ -e "$WITHOUT/.claude-grok-worker/skills/$SKILL" ]] && echo YES-BAD || echo no)"
echo "with:    $(ls "$WITH/.claude-grok-worker/skills" | wc -l | tr -d ' ') skills, $SKILL present: $([[ -e "$WITH/.claude-grok-worker/skills/$SKILL" ]] && echo yes || echo NO-BAD)"
echo "live farm untouched: $(ls "$FARM" | wc -l | tr -d ' ') skills"
