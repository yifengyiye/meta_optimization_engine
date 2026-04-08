from fastapi import APIRouter

from app.config import get_settings
from app.schemas.input_models import AnalyzeRequest
from app.schemas.output_models import AnalyzeResponse, HealthResponse, RuleSummary
from app.services.recommendation_service import RecommendationService
from app.rules.meta_rule_loader import RuleLoader

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="ok",
        app_name=settings.app_name,
        app_version=settings.app_version,
        rule_version=settings.rule_version,
    )


@router.get("/rules", response_model=list[RuleSummary])
def rules() -> list[RuleSummary]:
    settings = get_settings()
    rule_loader = RuleLoader(settings.rules_path)
    loaded_rules = rule_loader.load_rules()
    return [
        RuleSummary(
            rule_id=rule.id,
            name=rule.name,
            category=rule.category,
            severity=rule.severity,
            action_type=rule.action_type,
            priority_score=rule.priority_score,
        )
        for rule in loaded_rules
    ]


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest) -> AnalyzeResponse:
    settings = get_settings()
    service = RecommendationService(settings.rules_path, settings.rule_version)
    return service.analyze(payload)

