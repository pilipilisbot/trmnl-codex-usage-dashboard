# Report an issue or suggest an improvement

First read the [installation guide](docs/INSTALL.md) and [troubleshooting guide](docs/TROUBLESHOOTING.md). Search [existing issues](https://github.com/pilipilisbot/trmnl-codex-usage-dashboard/issues) before opening a new one.

For a bug, [open an issue](https://github.com/pilipilisbot/trmnl-codex-usage-dashboard/issues/new) and include:

- What you expected and what happened.
- The exact command or installation step that failed, plus a minimal reproduction.
- Your OS, Python version (`python3 --version`), and Codex CLI version (`codex --version`).
- Whether `--dry-run` succeeds, whether a normal run says `delivered`, and which TRMNL layout/device is affected.
- The relevant **redacted** error and, for display bugs, a screenshot with personal usage and account names removed.

**Never include** a webhook URL, Codex auth file/token, `local/collector.json`, raw Codex sessions, prompts, project paths, or a screenshot exposing personal data. Replace the URL with `https://trmnl.com/api/custom_plugins/REDACTED` and account labels with generic names. A public issue is visible to everyone.

For feature requests, describe the use case and proposed behavior. For security-sensitive issues or exposed credentials, do **not** open a public issue: contact the repository maintainers privately through GitHub's [security advisory reporting](https://github.com/pilipilisbot/trmnl-codex-usage-dashboard/security/advisories/new) if available. Rotate any exposed webhook immediately in TRMNL.
