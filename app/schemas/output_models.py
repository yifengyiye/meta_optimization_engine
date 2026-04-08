from pydantic import BaseModel


class RuleSummary(BaseModel):
    rule_id: str
    name: str
    category: str
    severity: str
    action_type: str
    priority_score: int


class MatchedRuleResult(BaseModel):
    rule_id: str
    name: str
    category: str
    severity: str
    action_type: str
    recommendation: str
    rationale: str
    priority_score: int


class AnalysisResult(BaseModel):
    ad_id: str
    risk_level: str
    primary_action: str
    diagnosis_summary: str
    matched_rules: list[MatchedRuleResult]
    computed_metrics: dict[str, float | bool | None]


class AnalyzeResponse(BaseModel):
    engine_version: str
    rule_version: str
    analyzed_count: int
    results: list[AnalysisResult]


class HealthResponse(BaseModel):
    status: str
    app_name: str
    app_version: str
    rule_version: str

