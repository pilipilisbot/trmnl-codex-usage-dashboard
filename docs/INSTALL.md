# Install

## A. Create an installation

Until the Recipe is public, create a TRMNL Private Plugin using the **Webhook** strategy. Paste `templates/full.liquid` into the **Full** markup editor and `templates/form_fields.yml` into **Form Fields**. Set an optional account label, save, then copy this instance's webhook URL. The webhook URL is a credential: do not commit it or include it in screenshots.

When the Recipe is listed, use its **Install** button instead; select an account label for each installation. Install it again for another account, then copy that installation's separate webhook URL. A Recipe install receives template updates from its owner; a fork does not.

The source template currently implements **Full** view only. Leave half/quad views disabled until they have their own templates and are tested.

## B. Configure one or more local senders

```bash
mkdir -p local
cp payloads/instances.example.json local/instances.json
cp payloads/sample-webhook.json local/work.json
cp payloads/sample-webhook.json local/personal.json
$EDITOR local/instances.json
```

For each entry in `local/instances.json`, set its own `webhook_url` and `payload_file`. These paths are relative to the repository root unless absolute. The entire `local/` directory is git-ignored. Restrict file permissions if other local users can read your home directory.

```bash
python3 scripts/publish.py --config local/instances.json --instance work --dry-run
python3 scripts/publish.py --config local/instances.json --instance work
python3 scripts/publish.py --config local/instances.json --all
```

`--dry-run` validates without network requests. `--all` delivers each payload to its matching webhook; an error for one account does not skip the others. The sender exits nonzero if any delivery failed, does not print webhook URLs, and never contacts an OpenAI endpoint.

## C. Supply real data

Generate one JSON payload per account as described in [PAYLOAD.md](PAYLOAD.md). A local job may write these files and run `publish.py` on a schedule. TRMNL's standard webhook limit is 12 requests per hour and 5 kB stored data; this sender enforces the standard 5 kB limit. Choose a schedule of at least five minutes per instance, preferably 15–30 minutes.

There is no generic, authorized Codex usage API wired into this repository. The dashboard is a renderer and delivery tool, not an account-linking service. Do not put OpenAI tokens in TRMNL form fields or payloads.

For an existing single-instance `.env` setup, `scripts/push-webhook.sh <payload.json>` remains available; its payload must use the new v2 contract.
