from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"


def test_analyze():
    payload = {
        "records": [
            {
                "date": "2026-04-07",
                "account_id": "a1",
                "campaign_id": "c1",
                "adset_id": "s1",
                "ad_id": "ad1",
                "spend": 120,
                "impressions": 10000,
                "clicks": 20,
                "link_clicks": 18,
                "landing_page_views": 5,
                "add_to_cart": 0,
                "initiate_checkout": 0,
                "purchases": 0,
                "revenue": 0
            }
        ]
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["analyzed_count"] == 1

