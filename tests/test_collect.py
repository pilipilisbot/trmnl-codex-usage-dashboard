import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import collect


class CollectorTests(unittest.TestCase):
    def test_official_rate_limit_response_and_local_aggregates(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            home = root / "codex-home"
            sessions = home / "sessions" / "2026" / "11" / "18"
            sessions.mkdir(parents=True)
            codex = root / "fake-codex"
            codex.write_text("""#!/usr/bin/env python3
import json, sys
requests = [json.loads(sys.stdin.readline()) for _ in range(3)]
assert requests[0]['method'] == 'initialize'
assert requests[2]['method'] == 'account/rateLimits/read'
result = {'rateLimits': {'primary': {'usedPercent': 64.2, 'windowDurationMins': 300, 'resetsAt': 1795006800}, 'secondary': {'usedPercent': 21, 'windowDurationMins': 10080, 'resetsAt': 1795611600}}}
print(json.dumps({'id': 1, 'result': {}}), flush=True)
print(json.dumps({'id': 2, 'result': result}), flush=True)
""", encoding="utf-8")
            codex.chmod(0o755)
            events = [
                {"timestamp": "2026-11-18T10:00:00Z", "type": "turn_context", "payload": {"model": "gpt-5.2-codex", "secret": "NEVER_SEND"}},
                {"timestamp": "2026-11-18T10:01:00Z", "type": "event_msg", "payload": {"type": "token_count", "info": {"total_token_usage": {"total_tokens": 1200}}}},
                {"timestamp": "2026-11-18T10:02:00Z", "type": "event_msg", "payload": {"type": "token_count", "info": {"total_token_usage": {"total_tokens": 2000}}}},
            ]
            (sessions / "sample.jsonl").write_text("\n".join(json.dumps(e) for e in events), encoding="utf-8")
            now = datetime(2026, 11, 18, 12, 0, tzinfo=timezone.utc)
            with patch.object(collect, "datetime") as mock_datetime:
                mock_datetime.now.return_value = now
                mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
                mock_datetime.fromisoformat.side_effect = datetime.fromisoformat
                payload = collect.build_payload({"codex_home": str(home), "codex_bin": str(codex), "account_label": "Work"}, now)
            data = payload["merge_variables"]
            self.assertEqual([row["used_pct"] for row in data["quotas"]], [64, 21])
            self.assertEqual(data["daily_usage"][-1]["pct"], 100)
            self.assertEqual(data["models"][0]["value"], "2.0k")
            self.assertEqual(data["recent"], [{"label": "18 Nov", "value": "2.0k"}])
            self.assertNotIn("NEVER_SEND", json.dumps(payload))
            self.assertNotIn(str(home), json.dumps(payload))

    def test_no_quota_does_not_send(self):
        with tempfile.TemporaryDirectory() as temp:
            entry = {"codex_home": temp, "webhook_url": "https://trmnl.com/api/custom_plugins/example"}
            with patch.object(collect, "rpc_rate_limits", return_value={"rateLimits": {}}), patch.object(collect.urllib.request, "urlopen") as send:
                with self.assertRaises(ValueError):
                    collect.collect("work", entry, False)
                send.assert_not_called()

    def test_dry_run_does_not_send(self):
        entry = {"webhook_url": "https://trmnl.com/api/custom_plugins/example"}
        with patch.object(collect, "build_payload", return_value={"merge_variables": {"account_label": "Work", "updated_at": "18 Nov 12:00", "quotas": [], "daily_usage": [], "models": [], "recent": []}}), patch.object(collect.urllib.request, "urlopen") as send:
            collect.collect("work", entry, True)
            send.assert_not_called()


if __name__ == "__main__":
    unittest.main()
