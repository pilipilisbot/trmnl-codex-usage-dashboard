# Publishing Options

There are three practical ways to ship this dashboard on TRMNL.

## 1. Private Plugin

Best for personal use, demos, and early validation.

- User creates a TRMNL Private Plugin.
- User pastes `templates/full.liquid`.
- A local job or hosted job sends `merge_variables` to the plugin webhook.

Pros:

- Fastest path.
- No public review.
- No hosted app required if the user pushes data from their own machine.

Cons:

- Manual setup per user.
- Not discoverable in the marketplace.

## 2. Recipe

Best for a public, reusable plugin when no third-party auth or external per-user server flow is required.

TRMNL Recipes live inside TRMNL and are the preferred public path for simple plugins that can be expressed as template plus configuration.

Pros:

- More publishable than a Private Plugin.
- No OAuth or user data custody.
- Better fit if the data source can be simple and user-provided.

Cons:

- Less control than a full hosted integration.
- May not fit if Codex usage data requires a custom authenticated exporter.

## 3. Third Party Plugin

Best for a polished marketplace integration with hosted install/manage flows.

TRMNL public plugin clients require:

- Installation URL.
- Installation success webhook URL.
- Plugin management URL.
- Plugin markup URL.
- Uninstallation webhook URL.
- Icon, name, and description.

Pros:

- Proper marketplace-style integration.
- Can handle account linking, hosted data collection, and richer management.

Cons:

- Requires a hosted service.
- Requires privacy/security work.
- More review and maintenance.

## Recommendation For This Project

Start with Private Plugin because it validates the screen and payload contract quickly.

For public release, target Recipe if users can provide the payload via webhook or a simple polling endpoint. Move to Third Party Plugin only if the dashboard needs hosted Codex account linking, user management, or automatic collection that cannot be done cleanly by a user-owned script.
