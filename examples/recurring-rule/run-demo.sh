#!/usr/bin/env bash
# Proves the recurring failure is invisible without the rule (red), then
# visible and rejected with the rule (green). Static linting only: this is a
# guardrail, not a security boundary, and it cannot prove all bypasses impossible.
set -uo pipefail
cd "$(dirname "$0")"

ESLINT="./node_modules/.bin/eslint"
mkdir -p evidence

if [ ! -x "$ESLINT" ]; then
  echo "eslint is not installed. Run: npm install   (pins eslint 10.10.0 and writes package-lock.json)" >&2
  exit 2
fi

echo "== RED: restriction absent, offending import passes silently =="
set +e
npm run --silent lint:red > evidence/red.txt 2>&1
RED=$?
set -e
cat evidence/red.txt
echo "red exit code: $RED"
if [ "$RED" -ne 0 ]; then
  echo "UNEXPECTED: lint without the rule must pass (exit 0) for the failure to be proven invisible." >&2
  exit 1
fi

echo
echo "== GREEN: restriction enabled, direct db import in src/ui rejected =="
set +e
npm run --silent lint > evidence/green.txt 2>&1
GREEN=$?
set -e
cat evidence/green.txt
echo "green exit code: $GREEN"
if [ "$GREEN" -ne 1 ]; then
  echo "UNEXPECTED: expected lint rejection exit 1; a config/runtime error is not acceptance." >&2
  exit 1
fi

grep -q "src/ui/UserCard.js" evidence/green.txt || { echo "UNEXPECTED: offending file not named in output." >&2; exit 1; }
grep -q "no-restricted-imports" evidence/green.txt || { echo "UNEXPECTED: rule id not reported." >&2; exit 1; }
if grep -q "src/ui/UserList.js" evidence/green.txt; then
  echo "UNEXPECTED: approved API import was flagged." >&2
  exit 1
fi

echo
echo "PASS: red evidence preserved in evidence/red.txt; green shows exactly the"
echo "src/ui database import rejected, approved API imports untouched."
