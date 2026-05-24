# WebAgentFlow Fixture Site

Internal deterministic fixture site for WebAgentFlow validation and regression.

This repository was extracted from:

```text
leechen298/WebAgentFlow/apps/validation-site
```

It also carries the minimal fixture API previously implemented under:

```text
leechen298/WebAgentFlow/apps/api/app/routers/validation_api.py
```

## Run

Install frontend dependencies:

```bash
pnpm install
```

Install backend dependencies:

```bash
cd server
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
cd ..
```

Start frontend and fixture API:

```bash
pnpm dev
```

Open:

```text
http://127.0.0.1:5175
```

## Build

```bash
pnpm build
```

## Contract

See `FIXTURE_CONTRACT.md`.

## Fixture Scenarios

See `docs/FIXTURE_SCENARIOS.md` for the current specs, implemented basic fixtures,
planned fixture families, and source scenario catalog.

## Migration Source

See `MIGRATION_SOURCE.md`.

## Source Planning Docs

Historical planning and review documents copied from WebAgentFlow are kept under
`docs/source/`. They preserve original monorepo paths as source context. They are
not current runtime instructions for this repository.
