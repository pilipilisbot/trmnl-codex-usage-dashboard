# Install and run

## 1. TRMNL installation

The Recipe is currently a draft. Until it is available to install, create a TRMNL Private Plugin with the **Webhook** strategy. Paste `templates/full.liquid` into Full markup and `templates/form_fields.yml` into Form Fields, then save. Copy the generated webhook URL for *that installation*. The URL acts like a credential: do not commit or share it.

When the Recipe becomes available, install it once for each account. Every installation generates a different webhook URL. You do **not** need to put an OpenAI token or password in TRMNL.

## 2. Local collector

Run on a Mac/Linux machine where the official Codex CLI is installed and logged in. The same machine must keep running for scheduled refreshes.

```bash
codex --version
mkdir -p local
cp payloads/collector.example.json local/collector.json
chmod 600 local/collector.json
$EDITOR local/collector.json
python3 scripts/collect.py --instance work --dry-run
python3 scripts/collect.py --instance work
```

Set `webhook_url` to the TRMNL installation URL. `codex_home` defaults to `~/.codex` and is the login whose quotas and sessions are read. `codex_bin` defaults to `codex`; set an absolute path if your scheduler has a minimal PATH. `account_label` is display text. The dry run contacts the Codex app-server for real quotas but does **not** send data to TRMNL. It prints only row counts, not credentials, webhook URLs or private session data.

For a second account, sign in with a separate Codex home and add another config entry:

```bash
CODEX_HOME="$HOME/.codex-personal" codex login
python3 scripts/collect.py --all --dry-run
python3 scripts/collect.py --all
```

Set that entry's `codex_home` to `~/.codex-personal` and its *own* webhook URL. The collector continues other installations if one fails. It rejects non-TRMNL destinations and does not print webhook URLs on errors.

## 3. Automatic refresh

Schedule `python3 /absolute/path/to/scripts/collect.py --config /absolute/path/to/local/collector.json --all` every 15 minutes using your system's scheduler (for example, `crontab -e` on Linux/macOS). Use absolute paths to both Python and the Codex binary. The standard TRMNL webhook permits 12 requests/hour per installation; 15 minutes is comfortably below this. Do not run multiple schedulers for the same instance. No service is installed or enabled automatically by this repository.

The collector requires network access to Codex's normal authenticated usage read and to the TRMNL webhook. It reads `~/.codex/sessions` locally, but sends only aggregate token counts, model names and quota figures—never prompts, replies, project paths, session IDs or credentials. The `local/` directory is git-ignored. Keep `local/collector.json` mode 600.

If Codex CLI is missing, auth has expired or no quota window is returned, the run fails and sends nothing; it does not substitute invented usage. For API-key logins, Codex's ChatGPT rate-limit read may be unavailable. Empty local session activity is valid and only affects the activity panels.

For manual/demo JSON delivery, see `scripts/publish.py` and [payload contract](PAYLOAD.md).
