from pathlib import Path
from pprint import pprint

from app.schemas.input_models import AnalyzeRequest, AdRecord
from app.services.recommendation_service import RecommendationService


def main():
    service = RecommendationService(
        Path(__file__).resolve().parents[1] / "app" / "rules" / "meta_rules.yaml",
        "demo-rule-version",
    )
    payload = AnalyzeRequest(
        records=[
            AdRecord(
                date="2026-04-07",
                account_id="a1",
                campaign_id="c1",
                adset_id="s1",
                ad_id="ad-demo-1",
                spend=180,
                impressions=12000,
                clicks=30,
                link_clicks=28,
                landing_page_views=9,
                add_to_cart=0,
                initiate_checkout=0,
                purchases=0,
                revenue=0,
            )
        ]
    )
    result = service.analyze(payload)
    pprint(result.model_dump())


if __name__ == "__main__":
    main()

