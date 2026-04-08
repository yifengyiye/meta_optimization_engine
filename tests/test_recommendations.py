from pathlib import Path

from app.schemas.input_models import AnalyzeRequest, AdRecord
from app.services.recommendation_service import RecommendationService


def test_recommendation_service_returns_results():
    service = RecommendationService(
        Path("app/rules/meta_rules.yaml"),
        "test-rule-version",
    )
    payload = AnalyzeRequest(
        records=[
            AdRecord(
                date="2026-04-07",
                account_id="a1",
                campaign_id="c1",
                adset_id="s1",
                ad_id="ad1",
                spend=200,
                impressions=10000,
                clicks=20,
                link_clicks=18,
                landing_page_views=8,
                add_to_cart=0,
                initiate_checkout=0,
                purchases=0,
                revenue=0,
            )
        ]
    )
    response = service.analyze(payload)
    assert response.analyzed_count == 1
    assert len(response.results) == 1

