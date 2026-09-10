#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

python3 build/check.py

if command -v node >/dev/null 2>&1 && NODE_PATH=build/node_modules node -e "require.resolve('puppeteer')" >/dev/null 2>&1; then
  NODE_PATH=build/node_modules node build/check-render.js
else
  echo "rendered check skipped: node or puppeteer not installed (cd build && npm install)"
fi
