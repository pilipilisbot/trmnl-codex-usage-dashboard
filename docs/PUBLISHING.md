# Marketplace path and release gate

## Decision

Publish as a **Recipe**, not a Third Party plugin. TRMNL describes Recipes as approved Private Plugins: public in its Recipes marketplace, with Liquid templates, custom form fields and independent installations, without the author hosting user data or a TRMNL OAuth server. This project now includes a local collector using the official Codex app-server usage read; users still run it themselves and provide their own per-installation webhook URL. No hosted account-linking service is needed.

Official references (checked 18 November 2026):

- [TRMNL plugin types](https://help.trmnl.com/en/articles/10546870-compare-custom-plugin-types)
- [Recipe creation, review and publication](https://help.trmnl.com/en/articles/10122094-plugin-recipes)
- [Private plugin webhook limits](https://docs.trmnl.com/go/private-plugins/webhooks)
- [Custom form fields](https://help.trmnl.com/en/articles/10513740-custom-plugin-form-builder)

A Third Party plugin would require a hosted installation, management, markup and uninstall service plus token storage and privacy controls. It is unnecessary for this self-hosted exporter model.

## Submission checklist

1. Create a clean **Webhook** Private Plugin in the TRMNL account; paste `templates/full.liquid` and `templates/form_fields.yml`.
2. Use only synthetic data from `payloads/sample-webhook.json` on the Recipe Master instance. TRMNL uses its latest screenshot as the public preview.
3. Verify the Full layout on the intended device sizes/orientations and confirm empty-data rendering. Do not claim half/quad support until those templates exist.
4. Verify the sender with two separate synthetic destinations locally. After the Recipe becomes installable, verify two actual installations with distinct labels, webhook URLs and payloads; confirm one account's data never appears in the other.
5. In the publication dialog, run **Ask trmy** and resolve its findings when available. Then select **Publish plugin?** and submit for public review. TRMNL manually approves Recipes; submission is not publication.

Do not submit before the live Full preview and synthetic webhook delivery have been proven on TRMNL. The public listing description should say: “Display real Codex quotas and local token activity with the included self-hosted collector; requires Codex CLI and a scheduled webhook sender.” Mention the setup guide and that the author receives no credentials.

## Current status (18 November 2026)

- Created the webhook Private Plugin **Codex Usage Dashboard** in the owner's TRMNL account (plugin setting `544833`). The Recipe Master uses only the synthetic `payloads/sample-webhook.json` data; the webhook returned HTTP 200. It remains a draft.
- Saved the Full markup and form fields, verified the live editor rendered all three quotas, seven bars, model rows, recent rows and the per-installation label. Fixed a quota-column overflow found in the first live preview. Set a generic icon and generated the marketplace preview from demo data.
- The **Ask trmy** pre-review returned layout/form-field requirements. Local source corrections are prepared, but they have not been applied to TRMNL after the owner paused publication.
- The owner's private plugin is active, with the current form fields and a synthetic webhook delivery returning HTTP 200. The first direct Python attempt returned HTTP 403; setting an identifying User-Agent fixed the request. The new local Codex collector is covered by a simulated app-server test; a live Codex CLI/account test remains pending because this agent environment has no `codex` executable. Do not present the collector as live-proven yet.
- Public marketplace submission and TRMNL human approval must be tracked separately. Do not describe the Recipe as publicly available until the listing is visible to other accounts.
- An actual second installation cannot be verified until TRMNL exposes the Recipe installation flow; the local sender's destination isolation is covered by tests. The owner will configure their real webhook and Codex home after the Recipe is available to install.

Once available, install once per account and use a different webhook URL and exporter payload for each. The Recipe Master should remain on synthetic demo data; never send personal usage to the master.
