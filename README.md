# Codex Usage for TRMNL

A reusable TRMNL Recipe candidate for displaying Codex usage on e-ink devices. Each installation has its own webhook, account label and data. The recipe does **not** collect OpenAI credentials or infer usage; the user runs an exporter of their choice and sends the documented payload.

## What it shows

Up to three named quotas, seven daily usage bars, four model rows and four recent-work rows. Empty sections render safely. The layout targets TRMNL's full 800×480 view.

## Install and publish

- [Install a private instance or Recipe](docs/INSTALL.md)
- [Payload contract and exporter responsibilities](docs/PAYLOAD.md)
- [Marketplace submission readiness](docs/PUBLISHING.md)

The source needed in TRMNL is `templates/full.liquid` plus `templates/form_fields.yml`. `payloads/sample-webhook.json` is synthetic demo data; it is not tied to an account.

## Multiple accounts

Install the Recipe once per account. TRMNL creates a distinct webhook URL for each instance. Keep those URLs in the ignored `local/instances.json` file and send separately:

```bash
mkdir -p local
cp payloads/instances.example.json local/instances.json
cp payloads/sample-webhook.json local/work.json
cp payloads/sample-webhook.json local/personal.json
$EDITOR local/instances.json
python3 scripts/publish.py --instance work --dry-run
python3 scripts/publish.py --all
```

Replace both example webhook URLs with the URLs shown by the corresponding TRMNL installations, and replace each sample payload with real data from that account. No cross-account aggregation occurs.

## Development

```bash
make validate
python3 -m unittest discover -s tests
```

## License

MIT
