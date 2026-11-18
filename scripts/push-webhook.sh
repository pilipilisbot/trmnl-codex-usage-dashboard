#!/usr/bin/env bash
set -euo pipefail

# Compatibility helper for a single installation. Prefer publish.py for multiple accounts.
if [ -f .env ]; then
  set -a
  # shellcheck disable=SC1091
  . ./.env
  set +a
fi

payload_path="${1:-${TRMNL_CODEX_PAYLOAD:-payloads/sample-webhook.json}}"
webhook_url="${TRMNL_CODEX_WEBHOOK_URL:-}"
if [ -z "$webhook_url" ]; then
  echo 'TRMNL_CODEX_WEBHOOK_URL is required' >&2
  exit 2
fi

python3 - "$payload_path" "$webhook_url" <<'PY'
import sys
from pathlib import Path
from publish import publish
publish("default", {"payload_file": str(Path(sys.argv[1]).resolve()), "webhook_url": sys.argv[2]}, False)
PY
