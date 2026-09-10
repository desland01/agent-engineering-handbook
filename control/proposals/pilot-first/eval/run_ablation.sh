#!/usr/bin/env bash
# Drive the full pilot-first ablation. See RUBRIC.txt, which is declared before this runs.
#
#     ./build_blind_sandbox.sh pilot-first
#     ./run_ablation.sh [n-per-side] [concurrency]
#
# Arms are interleaved c01,t01,c02,t02,... so if the upstream drifts or degrades partway
# through, both sides absorb it equally. Results append as one JSON line per arm.
set -euo pipefail

N="${1:-20}"
P="${2:-5}"
DIR="$(cd "$(dirname "$0")" && pwd)"
OUT="$DIR/results-$(date +%Y%m%d-%H%M%S).jsonl"

for target in "$HOME/.sandbox-eval-home" "$HOME/.sandbox-eval-home-with"; do
  [[ -d "$target/.claude-grok-worker/skills" ]] || {
    echo "missing $target — run ./build_blind_sandbox.sh pilot-first first" >&2; exit 2; }
done

echo "n=$N per side, concurrency=$P, results -> $OUT" >&2
for i in $(seq 1 "$N"); do
  printf 'c%02d control\nt%02d treatment\n' "$i" "$i"
done | xargs -P "$P" -L 1 "$DIR/run_arm.sh" | tee -a "$OUT"

echo "done: $(wc -l <"$OUT" | tr -d ' ') arms scored -> $OUT" >&2
