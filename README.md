# Codex Usage Dashboard for TRMNL

A TRMNL Recipe with a self-hosted collector for Codex usage. The collector reads quota windows from the official `codex app-server` API and optional aggregate token activity from local Codex session logs. It sends the resulting display data to **your own** TRMNL installation webhook. No OpenAI login or API key is entered in TRMNL or sent to the recipe author.

Quota percentages and reset times come from Codex. Daily bars and model mix are **relative local token activity**, not billing or remaining quota. If the Codex account does not expose rate-limit windows, the collector fails without sending a fabricated value.

## Install

The Recipe is currently **private**. Once its public TRMNL listing is approved, install **Codex Usage Dashboard** from TRMNL Recipes, copy the installation's webhook URL, and follow the [local collector installation guide](docs/INSTALL.md). You can install the Recipe once per Codex account; use a separate webhook and `CODEX_HOME` for each.

The source and a private-plugin testing path are available now. See [installation](docs/INSTALL.md), [troubleshooting](docs/TROUBLESHOOTING.md), and [how to report an issue](CONTRIBUTING.md).

## Development and release

`src/` is the TRMNL-synced Recipe; `templates/` is the maintained plain-text copy of its Liquid layouts and form fields. Run `make validate` and `python3 -m unittest discover -s tests` before changes. The [payload contract](docs/PAYLOAD.md) describes custom senders; [publication checklist](docs/PUBLISHING.md) tracks the marketplace release. The sample payload is synthetic.

## License

MIT
