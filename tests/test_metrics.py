from app.schemas.input_models import AdRecord
from app.services.metric_service import MetricService


def test_compute_metrics_basic():
    service = MetricService()
    record = AdRecord(
        date="2026-04-07",
        account_id="a1",
        campaign_id="c1",
        adset_id="s1",
        ad_id="ad1",
        spend=100,
        impressions=10000,
        clicks=200,
        link_clicks=150,
        landing_page_views=120,
        add_to_cart=12,
        initiate_checkout=6,
        purchases=2,
        revenue=300,
    )
    metrics = service.compute_metrics(record)
    assert metrics["ctr"] == 0.02
    assert metrics["cpm"] == 10
    assert metrics["roas"] == 3

