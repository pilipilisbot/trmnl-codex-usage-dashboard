#!/usr/bin/env python3
"""Validate and send independent Codex usage payloads to TRMNL installations."""

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
MAX_BYTES = 5000
USER_AGENT = "CodexUsageTRMNL/1.0 (+https://github.com/pilipilisbot/trmnl-codex-usage-dashboard)"


def read_json(path):
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_payload(payload):
    if not isinstance(payload, dict) or set(payload) != {"merge_variables"}:
        raise ValueError("payload must contain only merge_variables")
    data = payload["merge_variables"]
    if not isinstance(data, dict):
        raise ValueError("merge_variables must be an object")
    required = {"updated_at", "quotas", "daily_usage", "models", "recent"}
    if not required <= data.keys():
        raise ValueError("missing fields: " + ", ".join(sorted(required - data.keys())))
    if set(data) - required - {"account_label"}:
        raise ValueError("unknown merge_variables fields")
    for key, maxlen in (("updated_at", 32), ("account_label", 32)):
        if key in data and (not isinstance(data[key], str) or len(data[key]) > maxlen):
            raise ValueError(f"{key} must be a string of at most {maxlen} characters")
    specs = {
        "quotas": (3, {"label": 32, "used": 20, "limit": 20, "reset": 32}, "used_pct"),
        "daily_usage": (7, {"label": 12}, "pct"),
        "models": (4, {"name": 24, "value": 12}, "pct"),
        "recent": (4, {"label": 24, "value": 12}, None),
    }
    for key, (maximum, strings, percent) in specs.items():
        rows = data[key]
        if not isinstance(rows, list) or len(rows) > maximum:
            raise ValueError(f"{key} must be an array with at most {maximum} items")
        expected = set(strings) | ({percent} if percent else set())
        for index, row in enumerate(rows):
            if not isinstance(row, dict) or set(row) != expected:
                raise ValueError(f"{key}[{index}] must contain exactly {sorted(expected)}")
            for field, maxlen in strings.items():
                if not isinstance(row[field], str) or len(row[field]) > maxlen:
                    raise ValueError(f"{key}[{index}].{field} must be a string of at most {maxlen} characters")
            if percent and (type(row[percent]) is not int or not 0 <= row[percent] <= 100):
                raise ValueError(f"{key}[{index}].{percent} must be an integer from 0 to 100")
    body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    if len(body) > MAX_BYTES:
        raise ValueError(f"payload is {len(body)} bytes, above the {MAX_BYTES}-byte standard TRMNL limit")
    return body


def validate_url(url):
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in {"trmnl.com", "www.trmnl.com"}:
        raise ValueError("webhook URL must use HTTPS on trmnl.com")
    if not parsed.path.startswith("/api/custom_plugins/") or len(parsed.path.split("/")) != 4 or not parsed.path.split("/")[3]:
        raise ValueError("webhook URL must be a TRMNL custom plugin URL")
    if parsed.username or parsed.password or parsed.port or parsed.query or parsed.fragment:
        raise ValueError("webhook URL cannot contain credentials, query or fragment")
    return url


def publish(name, entry, dry_run):
    if not isinstance(entry, dict) or set(entry) != {"webhook_url", "payload_file"}:
        raise ValueError(f"{name}: expected webhook_url and payload_file")
    url = validate_url(entry["webhook_url"])
    payload_path = Path(entry["payload_file"])
    if not payload_path.is_absolute():
        payload_path = ROOT / payload_path
    body = validate_payload(read_json(payload_path))
    if dry_run:
        print(f"{name}: valid ({len(body)} bytes); no request sent")
        return
    request = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json", "User-Agent": USER_AGENT}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            if response.status != 200:
                raise RuntimeError(f"TRMNL returned HTTP {response.status}")
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"TRMNL returned HTTP {error.code}") from None
    print(f"{name}: delivered")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "local" / "instances.json")
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--instance", help="publish one named installation")
    scope.add_argument("--all", action="store_true", help="publish every installation")
    parser.add_argument("--dry-run", action="store_true", help="validate without sending")
    args = parser.parse_args()
    config = read_json(args.config)
    if not isinstance(config, dict) or not isinstance(config.get("instances"), dict):
        raise ValueError("config must contain an instances object")
    instances = config["instances"]
    if args.instance:
        if args.instance not in instances:
            raise ValueError(f"unknown instance: {args.instance}")
        selected = [(args.instance, instances[args.instance])]
    else:
        selected = list(instances.items())
    if not selected:
        raise ValueError("no instances configured")
    failed = False
    for name, entry in selected:
        try:
            publish(name, entry, args.dry_run)
        except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as error:
            print(f"{name}: {error}", file=sys.stderr)
            failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)
