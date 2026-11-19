import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import publish


class PublishTests(unittest.TestCase):
    def test_sample_contract_and_size(self):
        body = publish.validate_payload(publish.read_json(publish.ROOT / "payloads/sample-webhook.json"))
        self.assertLessEqual(len(body), publish.MAX_BYTES)

    def test_invalid_percent_rejected(self):
        payload = publish.read_json(publish.ROOT / "payloads/sample-webhook.json")
        payload["merge_variables"]["quotas"][0]["used_pct"] = "120"
        with self.assertRaises(ValueError):
            publish.validate_payload(payload)

    def test_two_installations_keep_destinations_and_payloads_separate(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            urls = []
            for name in ("work", "personal"):
                payload = publish.read_json(publish.ROOT / "payloads/sample-webhook.json")
                payload["merge_variables"]["account_label"] = name
                (root / f"{name}.json").write_text(json.dumps(payload), encoding="utf-8")
            instances = {
                name: {"webhook_url": f"https://trmnl.com/api/custom_plugins/{name}", "payload_file": str(root / f"{name}.json")}
                for name in ("work", "personal")
            }

            class Response:
                status = 200
                def __enter__(self):
                    return self
                def __exit__(self, *_):
                    return False

            def capture(request, timeout):
                self.assertEqual(request.get_header("User-agent"), publish.USER_AGENT)
                urls.append((request.full_url, json.loads(request.data)["merge_variables"]["account_label"]))
                return Response()

            with patch.object(publish.urllib.request, "urlopen", side_effect=capture):
                for name, entry in instances.items():
                    publish.publish(name, entry, False)
            self.assertEqual(urls, [
                ("https://trmnl.com/api/custom_plugins/work", "work"),
                ("https://trmnl.com/api/custom_plugins/personal", "personal"),
            ])

    def test_reject_non_trmnl_destination(self):
        with self.assertRaises(ValueError):
            publish.validate_url("https://example.com/api/custom_plugins/id")


if __name__ == "__main__":
    unittest.main()
