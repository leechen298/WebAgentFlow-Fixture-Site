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
# Requires the Fixture-Site dev server.
pnpm run test:browser-smoke

# Local-only legacy integration helper. Requires explicit opt-in because it
# writes raw fixture details into a WebAgentFlow developer checkout.
python3 evals/seed-webagentflow-replay-fixtures.py --webagentflow-local-seed
```

With `--webagentflow-local-seed`, `seed-webagentflow-replay-fixtures.py`
writes replay fixture ids and raw local target context to the WebAgentFlow
checkout's ignored `apps/e2e/.tmp/replay-fixtures.json`. That path is a
legacy local E2E helper only; it is not the provider summary artifact and must
not be committed to WebAgentFlow.

When a fixture-specific runner is added here, it should emit a redacted summary
that WebAgentFlow can validate against its generic external eval result schema.
Raw browser traces, screenshots, and provider-specific manifests should stay in this repository unless they are explicitly redacted.

## Provider-Owned Cases

Detailed pass, failure, selector, browser smoke, and replay seed cases live in:

```text
evals/provider-cases.md
```

These cases may mention fixture routes, selectors, and seed values because they
belong to this repository. Do not copy those details into WebAgentFlow.

## External Provider Result Contract

Fixture-Site writes the redacted summary intended for WebAgentFlow consumption
to:

```text
evals/artifacts/latest/provider-summary.redacted.json
```

Generate it after provider-owned checks:

```bash
pnpm run eval:provider
```

The summary follows WebAgentFlow's `waf.eval.result.v1` schema and uses only:

- `provider.kind = fixture_site`
- opaque `target.target_ref`
- opaque `case_results[].case_id`
- aggregate `status`
- `redacted: true` metadata

It must not contain fixture routes, selectors, ids, classes, seed values,
screen captures, DOM, raw Playwright output, WebAgentFlow internal execution
payloads, credentials, tokens, or cookies.

`eval:summary` accepts only fixed command ids such as `provider-full`; it does
not copy arbitrary shell commands into the redacted artifact.
