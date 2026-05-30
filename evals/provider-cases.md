# Provider-Owned Verification Cases

This file is intentionally kept in WebAgentFlow-Fixture-Site. It contains
fixture routes, selectors, and expected fixture behavior that must not be
copied into WebAgentFlow product runtime, default docs, or target-agnostic
tests.

## Required Local Gates

Run these gates before publishing a Fixture-Site provider result:

```bash
pnpm run test:selectors
pnpm run test:browser-smoke
pnpm run eval:provider
```

`test:browser-smoke` requires the Fixture-Site frontend and fixture API to be
running. It uses `WAF_FIXTURE_SITE_URL` when set, otherwise it targets the
local fixture frontend.

## Selector Stability Cases

These cases validate that authored fixture selectors remain stable for
WebAgentFlow regression providers.

| Case | Purpose | Gate |
|---|---|---|
| `fixture-selector-login-stability` | Login controls and error region keep stable selectors. | `pnpm run test:selectors` |
| `fixture-selector-users-search-stability` | User directory search controls keep stable selectors. | `pnpm run test:selectors` |
| `fixture-selector-users-result-stability` | User result and detail selectors keep stable markers. | `pnpm run test:selectors` |
| `fixture-selector-dashboard-stability` | Dashboard success marker remains stable. | `pnpm run test:selectors` |

## Browser Smoke Cases

These are provider-owned browser cases. They are allowed to mention fixture
routes, fixture labels, selectors, and seed values because they stay in this
repository.

| Case | Route | Purpose | Expected result |
|---|---|---|---|
| `fixture-browser-login-render` | `/login` | Render the login page and key controls. | Page shows username, password, and submit controls with no alert. |
| `fixture-browser-login-invalid-credentials` | `/login` | Exercise the negative credential path. | Page stays on login and shows the deterministic alert. |
| `fixture-browser-users-render` | `/users` | Render the user directory with seeded data. | Search controls, result card, table, and seeded user are visible. |
| `fixture-browser-users-search-name` | `/users` | Search by name. | URL carries the name query and the matching seeded user remains visible. |
| `fixture-browser-users-search-no-match` | `/users` | Search with a value that matches no seeded user. | URL carries the name query and the empty state is visible. |

## Replay Seed Cases

`evals/seed-webagentflow-replay-fixtures.py` is a legacy provider-owned local
integration helper. It is not part of the provider result contract and is not
run by default.

The script requires explicit opt-in:

```bash
python3 evals/seed-webagentflow-replay-fixtures.py --webagentflow-local-seed
```

With that opt-in, it writes raw fixture details to WebAgentFlow's ignored local
developer path:

```text
apps/e2e/.tmp/replay-fixtures.json
```

That file is local-only input for legacy WebAgentFlow E2E. It is not a
redacted provider result and must not be committed to WebAgentFlow. It must not
be used as evidence that WebAgentFlow only consumed provider summaries.

## Redacted Result Summary

The only artifact intended for WebAgentFlow consumption is:

```text
evals/artifacts/latest/provider-summary.redacted.json
```

The summary uses opaque case ids, aggregate statuses, and redaction metadata.
It must not contain fixture routes, selectors, user seed values, screenshots,
DOM, traces, raw Playwright output, or WebAgentFlow internal payloads.
