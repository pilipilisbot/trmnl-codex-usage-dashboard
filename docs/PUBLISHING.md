# TRMNL Recipe publication checklist

TRMNL Recipes are reviewed public versions of Private Plugins. This project uses the **Webhook** strategy and a user-run local collector; it does not need a hosted OAuth or account-linking service. References: [Recipes](https://help.trmnl.com/en/articles/10122094-plugin-recipes), [plugin types](https://help.trmnl.com/en/articles/10546870-compare-custom-plugin-types), and [webhooks](https://docs.trmnl.com/go/private-plugins/webhooks).

## Verified on 19 November 2026

- The private Recipe (`544833`) renders Full, Half Horizontal, Half Vertical, and Quadrant. TRMNL's trmy review checked OG, X landscape, X portrait, and 1-bit and returned **“All checks passed, no notes.”**
- The owner tested real data on their device and confirmed it works. The saved OG and TRMNL X marketplace images use only synthetic demo data. The Recipe Master's personal feed was restored after image generation. Its visible account label was subsequently changed to the neutral `Work account`; the saved marketplace images still show only `Codex demo`. Webhook data sharing remains disabled.
- The collector has local contract tests for quota parsing, payload validation, destination isolation, no-send on missing quotas, and dry-run behavior. **A live collector run in this agent environment is not verified** because the Codex CLI is unavailable here; the owner's working device is the real-data check.
- The repository is public. TRMNL Sync is restricted to this repository; the synced `src/settings.yml` uses the webhook strategy and contains no credentials. TRMNL saves automatically to GitHub; GitHub changes require a manual import into TRMNL.

## Marketplace preflight on 19 November 2026

Both saved featured images were regenerated from a synthetic payload and a temporary `Codex demo` display label. The OG and TRMNL X images are nonblank and visually inspected: no personal account label, real quota, webhook URL, or credential appears. The original private feed was restored and verified against a local backup. The account label was later replaced with the neutral `Work account` after trmy warned that a personal label could appear on public Recipe screens. The backup was not committed.

TRMNL Chef initially blocked submission for excess inline styling. The layouts now use native Framework utility classes for spacing and alignment; TRMNL Sync saved the submitted `src/` files to `main` in commit `c4ed76e`. Actual Framework spacing and flex classes were checked in the live renderer. One dynamic model meter was changed to a native `<progress>` element to pass Chef's inline-style limit. Both featured images were regenerated again from synthetic data after the final layout change and visually inspected. The owner's original private feed was restored and verified. The fresh trmy layout review requested at 13:16 UTC passed all four views and 1-bit with no clipping or layout issues. Its only privacy note—the personal account label—was resolved by changing the visible label to `Work account`; the current rendered preview was checked for the neutral label and absence of an email address.

## Before submission

1. Confirm the public repository's README, installation, troubleshooting, and issue-reporting links work. Check the latest `main` commit and that the Recipe's live layouts match it. Do not accidentally import a stale GitHub snapshot over the tested TRMNL version.
2. Keep only synthetic data in the Recipe Master's latest public-preview screenshot. Confirm no personal account labels, quota values, webhook URLs, or credentials are visible in the icon, screenshots, description, form fields, or repository.
3. Run `make validate` and `python3 -m unittest discover -s tests`; verify the four layouts and empty-data rendering in the TRMNL editor. Re-run **Ask trmy** if the layouts or form fields changed after its clean review.
4. Ensure the listing says that each user installs the Recipe, copies their own webhook, runs the local collector on a machine with Codex CLI, and schedules updates. Do not imply automatic account linking or hosted collection.
5. Submit the Recipe for TRMNL's human review using the publication control. **Submission is not approval or a public listing.** Record the review result and verify the listing from an unrelated account after approval.
6. After the public installation flow exists, test two real installations with distinct labels, webhook URLs, and Codex homes. Confirm no data crosses between them. This cannot be fully verified while the Recipe is private.

Current status: **submitted for TRMNL human review on 19 November 2026; not yet approved or public**. Chef's blocking checks passed; its remaining suggestions (title bar, layout class, inline `style`, and `<style>` block) were advisory and acknowledged. The editor confirms “Recipe under review.” Do not tell users to install it from the marketplace until the public listing is visible. Never include personal usage in saved marketplace images.
