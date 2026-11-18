#!/usr/bin/env python3
"""Collect Codex quotas and local activity, then deliver each TRMNL installation."""

import argparse
import json
import os
import select
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

from publish import read_json, validate_payload, validate_url
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def rpc_rate_limits(codex_bin, codex_home, timeout=25):
    """Ask the official Codex app-server; never read or transmit auth.json ourselves."""
    env = os.environ.copy()
    env["CODEX_HOME"] = str(codex_home)
    try:
        process = subprocess.Popen(
            [codex_bin, "app-server", "--listen", "stdio://"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            bufsize=0, env=env,
        )
    except FileNotFoundError:
        raise ValueError(f"Codex CLI not found: {codex_bin}") from None
    deadline = time.monotonic() + timeout
    pending = b""
    try:
        requests = [
            {"id": 1, "method": "initialize", "params": {"clientInfo": {"name": "trmnl-codex-usage", "version": "1.0.0"}}},
            {"method": "initialized"},
            {"id": 2, "method": "account/rateLimits/read", "params": {"excludeResetCreditDetails": True}},
        ]
        for request in requests:
            process.stdin.write((json.dumps(request, separators=(",", ":")) + "\n").encode())
            process.stdin.flush()
        while time.monotonic() < deadline:
            ready, _, _ = select.select([process.stdout], [], [], max(0, deadline - time.monotonic()))
            if not ready:
                break
            chunk = os.read(process.stdout.fileno(), 65536)
            if not chunk:
                break
            pending += chunk
            while b"\n" in pending:
                line, pending = pending.split(b"\n", 1)
                try:
                    response = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if response.get("id") != 2:
                    continue
                if "error" in response:
                    raise ValueError("Codex rate-limit read failed: " + str(response["error"].get("message", "unknown error")))
                result = response.get("result")
                if not isinstance(result, dict):
                    raise ValueError("Codex returned no rate-limit data")
                return result
        raise ValueError("Codex app-server did not answer the rate-limit request")
    finally:
        process.terminate()
        try:
            process.communicate(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()
            process.communicate()


def _clip(value, length):
    return str(value)[:length]


def _window_label(minutes, fallback):
    if not isinstance(minutes, (int, float)) or minutes <= 0:
        return fallback
    if minutes < 60:
        return f"{int(minutes)}m"
    if minutes < 1440:
        return f"{minutes / 60:g}h"
    return f"{minutes / 10080:g}w" if minutes % 10080 == 0 else f"{int(minutes / 1440)}d"


def quota_rows(result, now):
    buckets = result.get("rateLimitsByLimitId") or {}
    if not isinstance(buckets, dict):
        buckets = {}
    if not buckets and isinstance(result.get("rateLimits"), dict):
        buckets = {"codex": result["rateLimits"]}
    rows = []
    for bucket_id, snapshot in sorted(buckets.items(), key=lambda item: item[0] != "codex"):
        if not isinstance(snapshot, dict):
            continue
        bucket_name = snapshot.get("limitName") or ("Codex" if bucket_id == "codex" else bucket_id.replace("_", " ").title())
        for kind, fallback in (("primary", "short"), ("secondary", "long")):
            window = snapshot.get(kind)
            if not isinstance(window, dict):
                continue
            used = window.get("usedPercent")
            if not isinstance(used, (int, float)) or isinstance(used, bool) or not 0 <= used <= 100:
                continue
            duration = _window_label(window.get("windowDurationMins"), fallback)
            reset = window.get("resetsAt")
            reset_text = "—"
            if isinstance(reset, (int, float)) and reset > 0:
                reset_text = datetime.fromtimestamp(reset, now.tzinfo).strftime("%d %b %H:%M")
            rows.append({
                "label": _clip(f"{bucket_name} · {duration}", 32),
                "used_pct": round(used), "used": "Used", "limit": f"{duration} window", "reset": reset_text,
            })
            if len(rows) == 3:
                return rows
    return rows


def activity_rows(codex_home, now):
    """Read only local session event counters; no prompts, replies, paths or IDs leave the host."""
    base = codex_home / "sessions"
    days = [(now.date() - timedelta(days=offset)) for offset in range(6, -1, -1)]
    daily = Counter()
    models = Counter()
    if base.is_dir():
        files = (p for p in base.rglob("*.jsonl") if p.is_file())
        for path in files:
            try:
                if path.stat().st_mtime < (now - timedelta(days=8)).timestamp() or path.stat().st_size > 20_000_000:
                    continue
                model = "Unknown"
                previous_total = 0
                with path.open(encoding="utf-8", errors="replace") as handle:
                    for line in handle:
                        try:
                            event = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        payload = event.get("payload") or {}
                        if event.get("type") == "turn_context" and isinstance(payload.get("model"), str):
                            model = payload["model"]
                        if event.get("type") != "event_msg" or payload.get("type") != "token_count":
                            continue
                        info = payload.get("info") or {}
                        total = (info.get("total_token_usage") or {}).get("total_tokens")
                        if not isinstance(total, int) or total < previous_total:
                            continue
                        delta = total - previous_total
                        previous_total = total
                        try:
                            date = datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00")).astimezone(now.tzinfo).date()
                        except (KeyError, ValueError, TypeError):
                            continue
                        if date in days and delta > 0:
                            daily[date] += delta
                            models[model] += delta
            except OSError:
                continue
    peak = max((daily[d] for d in days), default=0)
    bars = [{"label": d.strftime("%a"), "pct": round(100 * daily[d] / peak) if peak else 0} for d in days]
    total_models = sum(models.values())
    model_rows = [
        {"name": _clip(name, 24), "pct": round(100 * count / total_models), "value": _clip(f"{count / 1000:.1f}k", 12)}
        for name, count in models.most_common(4)
    ]
    recent = [{"label": d.strftime("%d %b"), "value": f"{daily[d] / 1000:.1f}k"} for d in reversed(days) if daily[d] > 0][:4]
    return bars, model_rows, recent


def build_payload(entry, now=None):
    now = now or datetime.now().astimezone()
    home = Path(entry.get("codex_home", "~/.codex")).expanduser().resolve()
    if not home.is_dir():
        raise ValueError(f"Codex home does not exist: {home}")
    limits = rpc_rate_limits(entry.get("codex_bin", "codex"), home)
    quotas = quota_rows(limits, now)
    if not quotas:
        raise ValueError("Codex returned no usable quota windows; refusing to send empty data")
    bars, models, recent = activity_rows(home, now)
    payload = {"merge_variables": {
        "account_label": _clip(entry.get("account_label", "Codex usage"), 32),
        "updated_at": now.strftime("%d %b %H:%M"),
        "quotas": quotas, "daily_usage": bars, "models": models, "recent": recent,
    }}
    validate_payload(payload)
    return payload


def collect(name, entry, dry_run):
    if not isinstance(entry, dict) or not isinstance(entry.get("webhook_url"), str):
        raise ValueError("webhook_url is required")
    url = validate_url(entry["webhook_url"])
    payload = build_payload(entry)
    body = validate_payload(payload)
    if dry_run:
        print(f"{name}: collected {len(payload['merge_variables']['quotas'])} quotas, {len(payload['merge_variables']['models'])} model rows; no TRMNL request sent")
        return
    request = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            if response.status != 200:
                raise RuntimeError(f"TRMNL returned HTTP {response.status}")
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"TRMNL returned HTTP {error.code}") from None
    print(f"{name}: delivered")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "local" / "collector.json")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--instance")
    group.add_argument("--all", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="collect and validate, without sending to TRMNL")
    args = parser.parse_args()
    config = read_json(args.config)
    instances = config.get("instances") if isinstance(config, dict) else None
    if not isinstance(instances, dict) or not instances:
        raise ValueError("config must contain a nonempty instances object")
    if args.instance and args.instance not in instances:
        raise ValueError(f"unknown instance: {args.instance}")
    selected = [(args.instance, instances[args.instance])] if args.instance else instances.items()
    failed = False
    for name, entry in selected:
        try:
            collect(name, entry, args.dry_run)
        except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as error:
            print(f"{name}: {error}", file=sys.stderr)
            failed = True
    return int(failed)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)
