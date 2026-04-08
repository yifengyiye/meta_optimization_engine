from app.rules.meta_rule_loader import RuleLoader
from app.schemas.input_models import AnalyzeRequest
from app.schemas.output_models import AnalyzeResponse, AnalysisResult, MatchedRuleResult
from app.services.ingestion_service import IngestionService
from app.services.metric_service import MetricService
from app.services.normalization_service import NormalizationService
from app.services.rule_engine import RuleEngine


class RecommendationService:
    def __init__(self, rules_path, rule_version: str):
        self.rule_loader = RuleLoader(rules_path)
        self.rule_engine = RuleEngine()
        self.metric_service = MetricService()
        self.normalization_service = NormalizationService()
        self.ingestion_service = IngestionService()
        self.rule_version = rule_version
        self.engine_version = "0.1.0"

    def _risk_from_rules(self, matched_rules) -> str:
        if not matched_rules:
            return "low"
        severities = [rule.severity for rule in matched_rules]
        if "critical" in severities:
            return "critical"
        if "high" in severities:
            return "high"
        if "medium" in severities:
            return "medium"
        return "low"

    def _primary_action(self, matched_rules) -> str:
        if not matched_rules:
            return "OBSERVE"
        return sorted(matched_rules, key=lambda x: x.priority_score, reverse=True)[0].action_type

    def _action_priority(self, action_type: str) -> int:
        priorities = {
            "FIX_TRACKING": 100,
            "PAUSE": 95,
            "FIX_PAYMENT": 90,
            "FIX_CHECKOUT": 85,
            "FIX_LANDING_PAGE": 80,
            "REPLACE_CREATIVE": 70,
            "IMPROVE_AOV": 60,
            "EXPAND_AUDIENCE": 55,
            "CONTROL_BUDGET": 50,
            "PREPARE_STOP": 45,
            "OPTIMIZE": 40,
            "SCALE": 30,
            "OBSERVE": 10,
        }
        return priorities.get(action_type, 0)

    def _dedupe_rules(self, matched_rules):
        deduped = {}
        for rule in matched_rules:
            key = (rule.action_type, rule.category, rule.recommendation)
            current = deduped.get(key)
            if current is None or rule.priority_score > current.priority_score:
                deduped[key] = rule
        return list(deduped.values())

    def _sort_rules(self, matched_rules):
        return sorted(
            matched_rules,
            key=lambda rule: (
                self._action_priority(rule.action_type),
                rule.priority_score,
            ),
            reverse=True,
        )

    def _build_summary(self, matched_rules, metrics: dict[str, float | bool | None]) -> str:
        if not matched_rules:
            return "No rule matched. Continue observing."

        top_rule = matched_rules[0]
        category_map = {
            "click": "点击层",
            "delivery": "曝光层",
            "landing_page": "承接层",
            "conversion": "承接层",
            "checkout": "结账层",
            "purchase": "支付/成交层",
            "profitability": "收益层",
            "data": "数据层",
            "fatigue": "素材疲劳层",
            "scale": "扩量层",
            "retargeting": "再营销层",
            "social_proof": "信任层",
        }
        layer = category_map.get(top_rule.category, "投放层")
        metric_fragments = []
        for key in ("ctr", "link_ctr", "lpv_rate", "add_to_cart_rate", "checkout_rate", "purchase_cvr", "cpa", "roas"):
            value = metrics.get(key)
            if value is not None:
                metric_fragments.append(f"{key}={value}")
                if len(metric_fragments) >= 3:
                    break
        metrics_text = ", ".join(metric_fragments)
        if metrics_text:
            return f"{layer}优先级最高。{top_rule.recommendation} 关键指标：{metrics_text}。"
        return f"{layer}优先级最高。{top_rule.recommendation}"

    def analyze(self, payload: AnalyzeRequest) -> AnalyzeResponse:
        rules = self.rule_loader.load_rules()
        records = self.ingestion_service.load_request(payload)
        results: list[AnalysisResult] = []

        for record in records:
            record = self.normalization_service.normalize_record(record)
            metrics = self.metric_service.compute_metrics(record)
            context = {**record.model_dump(), **metrics}
            matched = [rule for rule in rules if rule.enabled and self.rule_engine.matches(rule, context)]
            matched_deduped = self._dedupe_rules(matched)
            matched_sorted = self._sort_rules(matched_deduped)

            matched_output = [
                MatchedRuleResult(
                    rule_id=rule.id,
                    name=rule.name,
                    category=rule.category,
                    severity=rule.severity,
                    action_type=rule.action_type,
                    recommendation=rule.recommendation,
                    rationale=rule.rationale,
                    priority_score=rule.priority_score,
                )
                for rule in matched_sorted
            ]

            summary = self._build_summary(matched_sorted, metrics)
            results.append(
                AnalysisResult(
                    ad_id=record.ad_id,
                    risk_level=self._risk_from_rules(matched_sorted),
                    primary_action=self._primary_action(matched_sorted),
                    diagnosis_summary=summary,
                    matched_rules=matched_output,
                    computed_metrics=metrics,
                )
            )

        return AnalyzeResponse(
            engine_version=self.engine_version,
            rule_version=self.rule_version,
            analyzed_count=len(results),
            results=results,
        )
