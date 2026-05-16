#!/usr/bin/env bash
set -euo pipefail

if [ -f ".env" ]; then
  set -a
  # shellcheck disable=SC1091
  . ./.env
  set +a
fi

payload_path="${1:-${TRMNL_CODEX_PAYLOAD:-payloads/sample-webhook.json}}"

if [ -z "${TRMNL_CODEX_WEBHOOK_URL:-}" ]; then
  echo "TRMNL_CODEX_WEBHOOK_URL is required. Copy .env.example to .env and set your plugin webhook URL." >&2
  exit 2
fi

if [ ! -f "$payload_path" ]; then
  echo "Payload file not found: $payload_path" >&2
  exit 2
fi

python3 -m json.tool "$payload_path" >/dev/null

curl "$TRMNL_CODEX_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  --data @"$payload_path"

echo
