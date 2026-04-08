import json
from pathlib import Path

import pytest

from app.schemas.input_models import AnalyzeRequest, AdRecord
from app.services.recommendation_service import RecommendationService


ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = ROOT / "app" / "rules" / "meta_rules.yaml"
TEST_CASES_PATH = ROOT / "test_data" / "meta_ads_320_test_cases.json"


def load_cases() -> list[dict]:
    payload = json.loads(TEST_CASES_PATH.read_text(encoding="utf-8"))
    return payload["cases"]


CASES = load_cases()


def allowed_actions(expected_action: str) -> set[str]:
    compatibility = {
        "SCALE_OR_BUDGET": {"SCALE", "EXPAND_AUDIENCE", "CONTROL_BUDGET", "OBSERVE"},
        "OPTIMIZE": {
            "OPTIMIZE",
            "REPLACE_CREATIVE",
            "FIX_LANDING_PAGE",
            "FIX_CHECKOUT",
            "FIX_PAYMENT",
            "IMPROVE_AOV",
            "EXPAND_AUDIENCE",
            "OBSERVE",
            "IMPROVE_OFFER_CLARITY",
        },
    }
    return compatibility.get(expected_action, {expected_action})


SERVICE = RecommendationService(RULES_PATH, "pytest-batch")


@pytest.mark.parametrize(
    "case",
    CASES,
    ids=[f"{case['case_id']}_rule_{case['source_rule_no']}" for case in CASES],
)
def test_generated_case_matches_expected_action(case: dict):
    request = AnalyzeRequest(records=[AdRecord(**case["record"])])
    response = SERVICE.analyze(request)
    result = response.results[0]

    expected = case["expected_primary_action"]
    allowed = allowed_actions(expected)

    assert result.primary_action in allowed, (
        f"case_id={case['case_id']} "
        f"rule_no={case['source_rule_no']} "
        f"metric={case['source_metric_text']} "
        f"expected={expected} "
        f"actual={result.primary_action} "
        f"summary={result.diagnosis_summary}"
    )
