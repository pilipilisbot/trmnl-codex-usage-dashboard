# Marketplace path and release gate

## Decision

Publish as a **Recipe**, not a Third Party plugin. TRMNL describes Recipes as approved Private Plugins: public in its Recipes marketplace, with Liquid templates, custom form fields and independent installations, without the author hosting user data or a TRMNL OAuth server. This project has no general-purpose OpenAI account-linking service, so pretending to offer automatic collection would mislead installers. Each user must supply data via their own exporter/webhook.

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
4. Verify two separate installations with different account labels, webhook URLs and payloads; confirm one account's data never appears in the other.
5. In the publication dialog, run **Ask trmy** and resolve its findings. Then select **Publish plugin?** and submit for public review. TRMNL manually approves Recipes; submission is not publication.

Do not submit before steps 1–4 have been proven on TRMNL. The public listing description should say: “Display Codex usage from your own exporter; requires a webhook sender.” Mention the setup guide and that the author receives no credentials.

## Current status

Repository code and docs are prepared, but this is **not yet a live Recipe**. A signed-in TRMNL session, rendered preview, multi-install test and moderation submission are still required. Do not claim marketplace publication until TRMNL lists it publicly.
