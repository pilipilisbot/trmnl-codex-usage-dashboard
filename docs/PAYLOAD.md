# Payload contract (v2)

The full example is [`payloads/sample-webhook.json`](../payloads/sample-webhook.json); JSON Schema is [`payloads/schema.json`](../payloads/schema.json). Send the complete object to the webhook using `Content-Type: application/json`. Every installation receives **only its own** account's payload.

```json
{
  "merge_variables": {
    "account_label": "Work account",
    "updated_at": "18 Nov 11:20",
    "quotas": [
      { "label": "5-hour quota", "used_pct": 63, "used": "3h 09m", "limit": "5h", "reset": "13:00" }
    ],
    "daily_usage": [{ "label": "Mon", "pct": 28 }],
    "models": [{ "name": "Model A", "pct": 71, "value": "14h" }],
    "recent": [{ "label": "Project A", "value": "1h 22m" }]
  }
}
```

`quotas` is an array of 0–3 cards, not fixed to a particular plan or product. If a quota is unavailable, omit its card; do not invent a limit. `daily_usage` accepts 0–7 bars, `models` and `recent` 0–4 rows. Percentages are integers 0–100. `display_name` in the TRMNL installation form takes precedence over the payload `account_label`; if neither is provided, the title is “Codex usage”. Text lengths and exact fields are constrained by the schema and the sender. The template HTML-escapes all account-controlled text.

The exporter is responsible for interpreting source data, the account's timezone, unit labels, and accurate quota resets. The display does not assert that usage percentages are official OpenAI billing or remaining quota. Use separate source credentials per account and keep them outside this repository and TRMNL.

The old v1 flat fields (`five_hour_*`, `weekly_*`, `spark_*`) are intentionally replaced by `quotas[]`. Exporters must migrate before sending to this version. The local validator fails closed on unknown fields to prevent silently displaying stale data.
