# Payload Contract

TRMNL expects webhook data under `merge_variables`.

Required top-level shape:

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
    "daily_usage": [],
    "models": [],
    "recent": []
  }
}
```

## Percent values

All `*_used_pct` fields and item `pct` fields are integers from 0 to 100.

## Arrays

- `daily_usage`: exactly 7 items looks best.
- `models`: 1-4 items.
- `recent`: 1-4 items.

Each `daily_usage` item:

```json
{ "label": "Mon", "pct": 28 }
```

Each `models` item:

```json
{ "name": "gpt-5.5", "pct": 71, "value": "14h" }
```

Each `recent` item:

```json
{ "label": "GitHub bridge", "value": "1h 22m" }
```
