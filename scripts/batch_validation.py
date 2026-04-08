import json
from collections import Counter
from pathlib import Path
from pprint import pprint
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.schemas.input_models import AnalyzeRequest, AdRecord
from app.services.recommendation_service import RecommendationService


RULES_PATH = ROOT / "app" / "rules" / "meta_rules.yaml"
TEST_CASES_PATH = ROOT / "test_data" / "meta_ads_320_test_cases.json"


def load_cases() -> list[dict]:
    payload = json.loads(TEST_CASES_PATH.read_text(encoding="utf-8"))
    return payload["cases"]


def run_validation() -> dict:
    service = RecommendationService(RULES_PATH, "batch-validation")
    cases = load_cases()
    summary = Counter()
    failures: list[dict] = []

    for case in cases:
        request = AnalyzeRequest(records=[AdRecord(**case["record"])])
        response = service.analyze(request)
        result = response.results[0]
        expected_action = case["expected_primary_action"]
        actual_action = result.primary_action

        # A few expected actions are intentionally broad; allow grouped matches.
        compatible = {
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
            },
        }
        allowed = compatible.get(expected_action, {expected_action})

        if actual_action in allowed:
            summary["passed"] += 1
        else:
            summary["failed"] += 1
            failures.append(
                {
                    "case_id": case["case_id"],
                    "rule_no": case["source_rule_no"],
                    "metric_text": case["source_metric_text"],
                    "expected": expected_action,
                    "actual": actual_action,
                    "diagnosis_summary": result.diagnosis_summary,
                }
            )

        summary["total"] += 1
        summary[f"actual::{actual_action}"] += 1
        summary[f"expected::{expected_action}"] += 1

    return {"summary": dict(summary), "failures": failures[:50]}


def main():
    report = run_validation()
    pprint(report["summary"])
    if report["failures"]:
        print("\nSample failures:")
        pprint(report["failures"][:10])
    else:
        print("\nAll cases passed.")


if __name__ == "__main__":
    main()
