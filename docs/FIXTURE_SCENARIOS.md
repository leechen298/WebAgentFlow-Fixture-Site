# Fixture Scenarios

This repository carries the internal deterministic fixture site extracted from WebAgentFlow.

## Auth / Listing Specs

Machine-readable and human-readable specs live in:

```text
web/specs/
```

Current specs:

- `login`
  - route: `/login`
  - scenarios: `valid_credentials`, `invalid_credentials`
- `users`
  - route: `/users`
  - scenarios: `filter_by_name`, `no_match`, `filter_by_status`

## Runtime Observation Fixtures

Current implemented basic fixtures:

- `basic-login`
- `basic-register`
- `basic-sms-login`
- `basic-search`
- `basic-detail`
- `basic-settings`
- `basic-confirm`

Source metadata:

```text
web/src/pages/runtime-observation/basic/basicFixtures.ts
```

## Planned Fixture Families

- Basic Business Pages
- Medium Business Pages
- Complex Business Pages
- Mobile Single-page Patterns
- Mock Backend Runtime Conditions

Source scenario catalog:

```text
docs/testing/scenarios/realistic-web-runtime-cases.md
```

## Historical Planning Docs

Copied from WebAgentFlow v0.1:

```text
docs/source/webagentflow-m11/
```

The copied `11.3.3-product-chat-test-site-separation` package is historical boundary context only.
It documents why validation-site and product-test-site were separated in the original monorepo.
This repository does not contain, migrate, or implement `apps/product-test-site`.

Historical docs under `docs/source/` may mention old monorepo paths such as `apps/validation-site`,
`apps/product-test-site`, and `docs/iterations/m11/`. Treat those paths as source context, not current
repository layout.
