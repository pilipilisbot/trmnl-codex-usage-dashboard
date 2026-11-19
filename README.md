# Codex Usage for TRMNL

A TRMNL Recipe and a **working local Codex collector**. Each installation has its own webhook URL and can point at a different `CODEX_HOME` (Codex login). No OpenAI credential goes to TRMNL.

## What it shows

Real Codex quota percentages and reset times from the official `codex app-server` `account/rateLimits/read` API. The local `~/.codex/sessions` logs supply seven days of relative token activity and model mix when available. The recent-activity panel shows token counts by day: project names and prompts are never sent to TRMNL. The local bars are relative activity, **not** quota or billing figures.

## Get started

1. Install and sign in to the [Codex CLI](https://github.com/openai/codex) on the machine that will run the collector. Confirm `codex --version` works.
2. Create or install a TRMNL Recipe instance and copy its *webhook URL*.
3. Copy the example config, set its webhook URL, and run the collector:

```bash
mkdir -p local
cp payloads/collector.example.json local/collector.json
$EDITOR local/collector.json
python3 scripts/collect.py --instance work --dry-run
python3 scripts/collect.py --instance work
```

See [installation and scheduling](docs/INSTALL.md). Run it every 15 minutes for automatic updates. To monitor another account, add an instance with its own webhook and separate `codex_home`; sign that home in with Codex CLI. One account's data never gets mixed with another's.

A **private test plugin** is active in the owner's TRMNL account; the Recipe is **not published in the marketplace**. The sample payload is synthetic. The original manual JSON sender remains available as `scripts/publish.py` for testing or custom exporters.

## Development

```bash
make validate
python3 -m unittest discover -s tests
```

## License

MIT
