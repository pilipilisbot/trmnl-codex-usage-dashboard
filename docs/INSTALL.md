# Install the local collector

Use this guide on a Mac or Linux machine that stays online for scheduled updates. It needs Python 3, the official [Codex CLI](https://github.com/openai/codex), an authenticated Codex account with available rate-limit data, and network access to TRMNL. No Python packages need installing.

## 1. Create a TRMNL installation

When the Recipe is public, find **Codex Usage Dashboard** in TRMNL Recipes and install it. Optionally set **Account label**. Save the installation, then copy its **Webhook URL** from the installation's settings. Each installation has a different URL; treat it as a password.

Until publication, the owner can test the [private plugin](https://trmnl.com/plugin_settings/544833/edit). Other testers can create a TRMNL Private Plugin with the **Webhook** strategy and copy all four Liquid layouts from `templates/` plus `templates/form_fields.yml` into the matching editor fields. Do not use the owner's private webhook.

## 2. Configure the collector

Install and log in to Codex CLI on the **same user account** that will run the collector. Confirm `codex --version` works and complete `codex login` if necessary. Then:

```bash
git clone https://github.com/pilipilisbot/trmnl-codex-usage-dashboard.git
cd trmnl-codex-usage-dashboard
mkdir -p local
cp payloads/collector.example.json local/collector.json
chmod 600 local/collector.json
${EDITOR:-vi} local/collector.json
```

Replace `REPLACE_WITH_YOUR_INSTANCE_UUID` in `webhook_url` with **your own full TRMNL webhook URL**. Keep the `https://trmnl.com/api/custom_plugins/...` form. `codex_home` is the Codex login to read (default `~/.codex`), `codex_bin` is the CLI executable (default `codex`), and `account_label` is display text. Set `codex_bin` to an absolute path if the scheduler cannot find it.

```bash
python3 scripts/collect.py --instance work --dry-run
python3 scripts/collect.py --instance work
```

The dry run reads real Codex quotas and local sessions but **does not post** to TRMNL. It prints row counts only. The second command sends the first payload. Check the installation's preview or regenerate its screen in TRMNL to confirm display. The webhook URL must stay in the git-ignored `local/collector.json`; never commit, post, or paste it into an issue.

## 3. Refresh automatically

Run the collector every 15 minutes. On macOS or Linux, one option is `crontab -e` with **absolute paths** to Python, this checkout, the config file, and the Codex executable in the config. For example, replace the paths below with those from `command -v python3`, `command -v codex`, and `pwd`:

```cron
*/15 * * * * /absolute/path/to/python3 /absolute/path/to/trmnl-codex-usage-dashboard/scripts/collect.py --config /absolute/path/to/trmnl-codex-usage-dashboard/local/collector.json --all
```

The TRMNL webhook allows 12 requests per hour per installation; every 15 minutes uses four. Do not schedule the same instance twice. This repository does not install a service or cron job for you. The machine and Codex login must remain available.

## 4. Monitor another Codex account

Create another TRMNL installation and copy **its** webhook. Sign in to the other Codex account using a separate home:

```bash
CODEX_HOME="$HOME/.codex-personal" codex login
```

Add another entry to `local/collector.json` with a distinct key, `codex_home` of `~/.codex-personal`, and its own webhook URL. Then run `python3 scripts/collect.py --all --dry-run` and `python3 scripts/collect.py --all`. A failure in one entry does not prevent attempts for other entries. Each account is collected and sent independently.

The collector sends quota figures, display labels, model names, and aggregate token counts. It never sends prompts, responses, project paths, session IDs, or Codex credentials. See [troubleshooting](TROUBLESHOOTING.md) if a run fails.
