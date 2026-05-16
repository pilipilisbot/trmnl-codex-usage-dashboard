# TRMNL Codex Usage Dashboard

Reusable TRMNL Private Plugin template for showing Codex usage and quota state on an e-ink dashboard.

The template is built for TRMNL OG's 800x480 black/white screen. It uses Liquid merge variables and simple CSS only: no runtime chart library, no color dependency, no external data collector baked into the template.

## Previewed Layout

- 5-hour quota card
- Weekly quota card
- Spark quota card
- 7-day usage bars
- Model usage breakdown
- Recent work breakdown

## Quickstart

```bash
git clone https://github.com/pilipilisbot/trmnl-codex-usage-dashboard.git
cd trmnl-codex-usage-dashboard
cp .env.example .env
$EDITOR .env
make validate
make push-sample
```

In TRMNL, create a Private Plugin with the Webhook strategy, paste `templates/full.liquid` into the Full markup view, then put the generated webhook URL in `.env` as `TRMNL_CODEX_WEBHOOK_URL`.

Full setup: `docs/INSTALL.md`.

## Files

- `templates/full.liquid` - paste this into TRMNL Private Plugin -> Markup -> Full.
- `payloads/sample-webhook.json` - sample webhook payload.
- `payloads/schema.json` - JSON Schema for the `merge_variables` payload.
- `scripts/push-webhook.sh` - sends any compatible payload to the TRMNL webhook.
- `Makefile` - `make validate` and `make push-sample` helpers.
- `.env.example` - local webhook configuration template.

## TRMNL Setup

1. Create a TRMNL Private Plugin.
2. Choose the Webhook strategy.
3. Paste `templates/full.liquid` into the Full markup view.
4. Save the plugin to get its webhook URL.
5. Send payloads shaped like `payloads/sample-webhook.json`.

```bash
curl "$TRMNL_CODEX_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  --data @payloads/sample-webhook.json
```

TRMNL webhook payloads must wrap dashboard variables under `merge_variables`:

```json
{
  "merge_variables": {
    "updated_at": "16 May 23:20",
    "five_hour_used_pct": 63,
    "five_hour_used": "3h 09m",
    "five_hour_limit": "5h",
    "five_hour_reset": "01:00",
    "weekly_used_pct": 42,
    "weekly_used": "18h",
    "weekly_limit": "42h",
    "weekly_reset": "Mon 00:00",
    "spark_used_pct": 25,
    "spark_used": "125",
    "spark_limit": "500",
    "spark_reset": "Mon 00:00",
    "daily_usage": [
      { "label": "Mon", "pct": 28 }
    ],
    "models": [
      { "name": "gpt-5.5", "pct": 71, "value": "14h" }
    ],
    "recent": [
      { "label": "GitHub bridge", "value": "1h 22m" }
    ]
  }
}
```

## Data Contract

Percent fields should be integers from 0 to 100. Keep arrays short so the payload stays within TRMNL webhook limits:

- `daily_usage`: 7 items
- `models`: up to 4 items
- `recent`: up to 4 items

The dashboard intentionally does not prescribe how Codex usage is collected. Feed it from whichever local exporter, billing API, CLI scrape, or scheduled job you trust.

## Publishing Notes

This repository is a template/source artifact for a TRMNL Private Plugin. To publish it as a community plugin, keep the template generic and document the data source used to produce the webhook payload.

## License

MIT
