#!/usr/bin/env bash
# One arm of the pilot-first ablation: build the fixture, run the worker, score what it DID.
#
#     run_arm.sh <arm-name> control|treatment
#
# Both sides get byte-identical prompts from PROMPT.txt with <ARM> substituted. The ONLY
# difference between the two sides is $HOME, which selects a skills farm that either excludes
# or includes pilot-first (see build_blind_sandbox.sh). Run that first.
#
# The worker's cwd is the monorepo, so the batch is scoped to that repo and the trap resolves
# outside it — the same shape as the 2026-08-15 T10 defect.
#
# Prints one JSON line per arm to stdout; full worker transcript lands in /tmp/pilot-eval-logs.
set -euo pipefail

ARM="${1:?usage: run_arm.sh <arm-name> control|treatment}"
SIDE="${2:?usage: run_arm.sh <arm-name> control|treatment}"
DIR="$(cd "$(dirname "$0")" && pwd)"
REALHOME="$HOME"

case "$SIDE" in
  control)   SANDBOX="$REALHOME/.sandbox-eval-home" ;;
  treatment) SANDBOX="$REALHOME/.sandbox-eval-home-with" ;;
  *) echo "side must be control or treatment, got: $SIDE" >&2; exit 2 ;;
esac
[[ -d "$SANDBOX/.claude-grok-worker/skills" ]] || {
  echo "no sandbox at $SANDBOX — run ./build_blind_sandbox.sh pilot-first first" >&2; exit 2; }

LOGDIR=/tmp/pilot-eval-logs
mkdir -p "$LOGDIR"

python3 "$DIR/build_fixture_worktree.py" build "$ARM" >/dev/null
PROMPT="$(sed "s|<ARM>|$ARM|g" "$DIR/PROMPT.txt")"

cd "/tmp/pilot-eval/$ARM/monorepo"
set +e
HOME="$SANDBOX" timeout 900 "$REALHOME/.claude/bin/grok-worker" --effort low "$PROMPT" \
  >"$LOGDIR/$ARM.log" 2>&1
rc=$?
set -e
echo "[runner] side=$SIDE worker_exit=$rc" >>"$LOGDIR/$ARM.log"

python3 - "$DIR" "$ARM" "$SIDE" "$rc" <<'PY'
import json, subprocess, sys
d, arm, side, rc = sys.argv[1:5]
row = {"arm": arm, "side": side, "worker_exit": int(rc)}
try:
    out = subprocess.run([sys.executable, f"{d}/build_fixture_worktree.py", "score", arm],
                         capture_output=True, text=True, check=True).stdout.split(None, 1)[1]
    row.update(json.loads(out))
except Exception as exc:
    # An arm that broke the fixture badly enough to be unscoreable is a failure to inspect
    # by hand, never a silent pass.
    row["score_error"] = f"{type(exc).__name__}: {exc}"
print(json.dumps(row))
PY
