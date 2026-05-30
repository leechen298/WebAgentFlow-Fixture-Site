#!/usr/bin/env python3
"""Seed WebAgentFlow LearnedPath replay fixtures from Fixture-Site.

This script intentionally lives in WebAgentFlow-Fixture-Site because it knows
Fixture-Site routes, selectors, seed values, and expected URLs. WebAgentFlow
consumes only the generated ``apps/e2e/.tmp/replay-fixtures.json`` result.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from sqlalchemy import delete


FIXTURE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WAF_ROOT = FIXTURE_ROOT.parent / "WebAgentFlow" / "v0.1"
WAF_REPO_ROOT = Path(os.environ.get("WAF_REPO_ROOT", DEFAULT_WAF_ROOT)).resolve()
API_ROOT = WAF_REPO_ROOT / "apps" / "api"
sys.path.insert(0, str(API_ROOT))

from app.core.db import SessionLocal  # noqa: E402
from app.models.learned_path import LearnedPath, Provenance, TrustStatus  # noqa: E402
from app.services.execution.execution_runtime import (  # noqa: E402
    RuntimeConfig,
    create_execution_runtime,
)
from app.services.learning.page_analyzer import analyze_page  # noqa: E402
from app.services.learning.page_signature import build_signature_dict  # noqa: E402


DEDUP_PREFIX = "e2e:replay:"
OUTPUT_PATH = WAF_REPO_ROOT / "apps" / "e2e" / ".tmp" / "replay-fixtures.json"


def _fixture_base_url() -> str:
    return (
        os.environ.get("WAF_FIXTURE_SITE_URL")
        or os.environ.get("E2E_FIXTURE_BASE_URL")
        or "http://127.0.0.1:5175"
    ).rstrip("/")


def _fixture_url(path: str) -> str:
    return f"{_fixture_base_url()}{path if path.startswith('/') else '/' + path}"


def _analyze_target_signature(target_url: str) -> dict[str, Any]:
    runtime = create_execution_runtime(config=RuntimeConfig(headless=True))
    runtime.start()
    try:
        runtime.navigate(target_url)
        analysis = analyze_page(runtime)
        current_url = runtime.current_url() if runtime.page else target_url
        return build_signature_dict(url=current_url, analysis=analysis)
    finally:
        runtime.stop()


def _happy_actions() -> list[dict[str, Any]]:
    return [
        {
            "step": 0,
            "action_type": "fill",
            "target_selector": "#search-name",
            "target_description": "Name input",
            "value": "alice",
        },
        {
            "step": 1,
            "action_type": "click",
            "target_selector": "#btn-search",
            "target_description": "Search button",
        },
    ]


def _row(
    *,
    name: str,
    scenario: str,
    purpose: str,
    trust: TrustStatus,
    signature: dict[str, Any],
    actions: list[dict[str, Any]],
    query_signature: dict[str, str] | None = None,
    page_template: str | None = None,
    dom_fingerprint: str | None = None,
) -> tuple[str, str, LearnedPath]:
    path = LearnedPath(
        page_template=page_template or str(signature["page_template"]),
        query_signature=query_signature
        if query_signature is not None
        else dict(signature["query_signature"]),
        dom_fingerprint=dom_fingerprint or str(signature["dom_fingerprint"]),
        scenario=scenario,
        actions=actions,
        provenance=Provenance.SYSTEM,
        trust=trust,
        hit_count=1,
        source_run_id=None,
        dedup_key=f"{DEDUP_PREFIX}{name}",
    )
    return name, purpose, path


def _build_rows(signature: dict[str, Any]) -> list[tuple[str, str, LearnedPath]]:
    return [
        _row(
            name="happy",
            scenario="e2e:replay:happy",
            purpose="confirmed provider replay happy path",
            trust=TrustStatus.CONFIRMED,
            signature=signature,
            actions=_happy_actions(),
        ),
        _row(
            name="observational",
            scenario="e2e:replay:observational",
            purpose="confirmed provider observational path with actions=[]",
            trust=TrustStatus.CONFIRMED,
            signature=signature,
            actions=[],
        ),
        _row(
            name="pageMismatch",
            scenario="e2e:replay:page-mismatch",
            purpose="stored provider path replayed against a mismatching page",
            trust=TrustStatus.CONFIRMED,
            signature=signature,
            actions=_happy_actions(),
        ),
        _row(
            name="targetMissing",
            scenario="e2e:replay:target-missing",
            purpose="supported action whose selector is absent",
            trust=TrustStatus.CONFIRMED,
            signature=signature,
            actions=[
                {
                    "step": 0,
                    "action_type": "fill",
                    "target_selector": "#e2e-replay-missing-target",
                    "target_description": "Missing input",
                    "value": "alice",
                }
            ],
        ),
        _row(
            name="unsupportedAction",
            scenario="e2e:replay:unsupported-action",
            purpose="unsupported action type is reported as drift evidence",
            trust=TrustStatus.CONFIRMED,
            signature=signature,
            actions=[
                {
                    "step": 0,
                    "action_type": "swipe",
                    "target_selector": "#search-name",
                    "target_description": "Name input",
                }
            ],
        ),
        _row(
            name="flaky",
            scenario="e2e:replay:flaky",
            purpose="flaky path can replay but reports a trust warning",
            trust=TrustStatus.FLAKY,
            signature=signature,
            actions=_happy_actions(),
        ),
        _row(
            name="deprecated",
            scenario="e2e:replay:deprecated",
            purpose="deprecated path returns HTTP 422",
            trust=TrustStatus.DEPRECATED,
            signature=signature,
            actions=_happy_actions(),
        ),
        _row(
            name="signatureChanged",
            scenario="e2e:replay:signature-changed",
            purpose="signature drift is non-blocking when selectors still match",
            trust=TrustStatus.CONFIRMED,
            signature=signature,
            query_signature={"e2e": "changed"},
            actions=_happy_actions(),
        ),
    ]


def main() -> None:
    target_url = _fixture_url("/users")
    mismatch_url = _fixture_url("/login")
    print(f"Analyzing Fixture-Site signature: {target_url}")
    signature = _analyze_target_signature(target_url)

    rows = _build_rows(signature)
    fixtures: dict[str, dict[str, str]] = {}

    with SessionLocal() as session:
        session.execute(
            delete(LearnedPath).where(LearnedPath.dedup_key.like(f"{DEDUP_PREFIX}%"))
        )
        for _name, _purpose, path in rows:
            session.add(path)
        session.commit()

        for name, purpose, path in rows:
            session.refresh(path)
            entry = {
                "id": str(path.id),
                "scenario": path.scenario,
                "trust": str(path.trust),
                "purpose": purpose,
                "target_url": target_url,
            }
            if name == "pageMismatch":
                entry["mismatch_url"] = mismatch_url
            if name in {"happy", "flaky", "signatureChanged"}:
                entry["expected_final_url_contains"] = f"{target_url}?name=alice"
            fixtures[name] = entry
            print(
                f"{name}: id={path.id} scenario={path.scenario} "
                f"trust={path.trust} purpose={purpose}"
            )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(
            {
                "generated_at": datetime.now(UTC).isoformat(),
                "provider": {"kind": "fixture_site", "name": "WebAgentFlow-Fixture-Site"},
                "fixtures": fixtures,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote fixture ids to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
