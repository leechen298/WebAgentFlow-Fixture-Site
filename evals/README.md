# Fixture-Specific Evals

Fixture-specific scenario runners, page selectors, seed values, and raw
artifacts belong in this repository, not in WebAgentFlow.

WebAgentFlow should consume only redacted result summaries and opaque case
results. It must not embed this site's routes, selectors, seed data, or answer
keys in product runtime code, default eval commands, or user-facing docs.

Current local checks:

```bash
pnpm run test:selectors
```

Optional provider-owned checks and seeders:

```bash
# Requires the Fixture-Site dev server and WebAgentFlow services.
python3 evals/seed-webagentflow-replay-fixtures.py

# Requires @playwright/test in the invoking environment.
pnpm exec playwright test evals/browser-smoke.spec.ts
```

`seed-webagentflow-replay-fixtures.py` writes opaque replay fixture ids and
target URLs to the WebAgentFlow checkout's ignored
`apps/e2e/.tmp/replay-fixtures.json`. WebAgentFlow E2E reads that generated
result but does not keep this repository's routes or selectors in its source.

When a fixture-specific runner is added here, it should emit a redacted summary
that WebAgentFlow can validate against its generic external eval result schema.
Raw browser traces, screenshots, and provider-specific manifests should stay in this repository unless they are explicitly redacted.
