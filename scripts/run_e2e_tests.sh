#!/usr/bin/env bash

FRONTEND_URL="http://localhost:3000/english-fight"

yarn --cwd=frontend start:e2e &
# wait till frontend compiles up to 3 min, with delay 10s (as it takes time) and interval 1s
yarn --cwd=frontend wait-on "$FRONTEND_URL" --delay 10000 --timeout 180000 --interval 1000 &&
  (cd backend && poetry run pytest tests/e2e)
#  braces to don't change current shell directory
#  See https://stackoverflow.com/a/786419/7119080