# Install

## 1. Clone

```bash
git clone https://github.com/pilipilisbot/trmnl-codex-usage-dashboard.git
cd trmnl-codex-usage-dashboard
```

## 2. Create the TRMNL Private Plugin

1. Open TRMNL.
2. Create a Private Plugin.
3. Select Webhook as the data strategy.
4. Paste `templates/full.liquid` into the Full markup editor.
5. Save the plugin.
6. Copy the generated webhook URL.

## 3. Configure the webhook URL

```bash
cp .env.example .env
$EDITOR .env
```

Set:

```bash
TRMNL_CODEX_WEBHOOK_URL=https://trmnl.com/api/custom_plugins/YOUR_PLUGIN_UUID
```

## 4. Test with sample data

```bash
make validate
make push-sample
```

Your TRMNL plugin should now render the sample dashboard.

## 5. Send real data

Generate a payload with the same shape as `payloads/sample-webhook.json`, then push it:

```bash
./scripts/push-webhook.sh path/to/your-payload.json
```

For scheduled updates, call the script from cron, systemd timer, GitHub Actions, or any local job that can produce the payload JSON.
