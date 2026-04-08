import json
from collections import Counter, defaultdict
from pathlib import Path
from pprint import pprint

from app.schemas.input_models import AnalyzeRequest, AdRecord
from app.services.recommendation_service import RecommendationService


ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = ROOT / "app" / "rules" / "meta_rules.yaml"
TEST_CASES_PATH = ROOT / "test_data" / "meta_ads_320_test_cases.json"


COMPATIBLE = {
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


def load_cases() -> list[dict]:
    payload = json.loads(TEST_CASES_PATH.read_text(encoding="utf-8"))
    return payload["cases"]


def run_report():
    service = RecommendationService(RULES_PATH, "analysis")
    cases = load_cases()
    summary = Counter()
    combos = Counter()
    metric_map = defaultdict(list)
    failures = []

    for case in cases:
        request = AnalyzeRequest(records=[AdRecord(**case["record"])])
        response = service.analyze(request)
        result = response.results[0]
        expected = case["expected_primary_action"]
        actual = result.primary_action
        allowed = COMPATIBLE.get(expected, {expected})

        summary[f"actual::{actual}"] += 1
        summary[f"expected::{expected}"] += 1
        summary["total"] += 1
        if actual not in allowed:
            summary["failed"] += 1
            combos[(expected, actual)] += 1
            metric_map[(expected, actual)].append(
                (case["case_id"], case["source_metric_text"], result.diagnosis_summary)
            )
            failures.append(
                {
                    "case_id": case["case_id"],
                    "rule_no": case["source_rule_no"],
                    "metric_text": case["source_metric_text"],
                    "expected": expected,
                    "actual": actual,
                }
            )
        else:
            summary["passed"] += 1

    return summary, combos, metric_map, failures


def main():
    summary, combos, metric_map, failures = run_report()
    pprint(dict(summary))
    pprint({k: v for k, v in combos.most_common(8)})
    for (expected, actual), hits in combos.most_common(5):
        print("\nMismatch group:", expected, "→", actual)
        for case_id, metric_text, diagnosis in metric_map[(expected, actual)][:3]:
            print(f"  {case_id} | {metric_text} | {diagnosis}")
    Path(ROOT / "test_output").mkdir(exist_ok=True)
    (ROOT / "test_output" / "failures.json").write_text(
        json.dumps(failures, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("\nDetailed failures written to test_output/failures.json")


if __name__ == "__main__":
    main()
