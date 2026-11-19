# Troubleshoot an installation

Run the exact failing instance manually before debugging a scheduler:

```bash
python3 scripts/collect.py --instance work --dry-run
```

| Symptom | What to check |
| --- | --- |
| `Codex CLI not found` | Run `codex --version` as the same OS user. Set `codex_bin` to the absolute path from `command -v codex`, especially for cron. |
| `Codex home does not exist` | Check `codex_home`, its expansion, and that the scheduler runs as the intended user. |
| No usable quota windows / rate-limit read failed | Complete `codex login` for that `CODEX_HOME`. An API-key login may not provide ChatGPT rate limits. Do not substitute guessed values. |
| App-server did not answer | Check that Codex CLI is current and can run as the scheduler user. Run the dry run interactively; an account or CLI problem may be hidden by cron's minimal environment. |
| `HTTP 403` or `HTTP 404` from TRMNL | Copy the webhook again from **this** installation, without extra characters. The URL may have changed or the installation may have been removed. Never post the URL publicly. |
| No activity bars or model rows | Local `CODEX_HOME/sessions` logs may be empty, unavailable, or older than seven days. Quota cards can still work. |
| Wrong account on screen | Check the `codex_home` and webhook pairing for each config entry. Each account needs its own TRMNL installation. |
| Dry run succeeds but screen stays old | Run without `--dry-run`, verify `delivered` appears, then check TRMNL's preview/screen refresh. Check that only one scheduler owns this installation. |
| Error only under cron | Use absolute paths for Python, `--config`, and `codex_bin`; run the cron command manually as the same user. |

The collector exits nonzero when any selected instance fails. It does not print webhook URLs, but inspect logs before sharing them. If this guide does not resolve the issue, [open a GitHub issue](../CONTRIBUTING.md) with a redacted error and reproduction steps.
