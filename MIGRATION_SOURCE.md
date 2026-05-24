# Migration Source

This repository was initially extracted from:

- Source repository: `leechen298/WebAgentFlow`
- Source ref: `v0.1`
- Source commit: `02c56e7e38208c8400391f882a07e7ef4aed534f`
- Frontend source path: `apps/validation-site`
- Fixture API source path: `apps/api/app/routers/validation_api.py`
- Scenario catalog source path: `docs/testing/scenarios/realistic-web-runtime-cases.md`
- Fixture planning source paths:
  - `docs/iterations/m11/11.2.4-realistic-scenario-catalog-fixture-planning`
  - `docs/iterations/m11/11.2.4.1-single-page-runtime-fixture-shell`
  - `docs/iterations/m11/11.2.4.2-single-page-basic-business-pages`
- Historical boundary source path: `docs/iterations/m11/11.3.3-product-chat-test-site-separation`

Initial purpose:

- Move the internal validation fixture site out of the WebAgentFlow main repository.
- Keep validation pages, authored specs, fixture UI, and fixture backend behavior together.
- Preserve WebAgentFlow main repository as runtime and eval protocol owner rather than validation-site source owner.

Boundary notes:

- Old `apps/validation-site` is now `web/`.
- Old `apps/api/app/routers/validation_api.py` is now `server/app/validation_api.py`.
- `apps/product-test-site` was not migrated and is not part of this repository.
- The copied `11.3.3-product-chat-test-site-separation` docs are historical boundary context only.
