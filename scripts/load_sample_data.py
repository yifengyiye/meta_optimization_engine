import json
from pathlib import Path


def main():
    sample = {
        "records": [
            {
                "date": "2026-04-07",
                "account_id": "a1",
                "campaign_id": "c1",
                "adset_id": "s1",
                "ad_id": "ad1",
                "spend": 100,
                "impressions": 10000,
                "clicks": 200,
                "link_clicks": 150,
                "landing_page_views": 120,
                "add_to_cart": 12,
                "initiate_checkout": 6,
                "purchases": 2,
                "revenue": 300
            }
        ]
    }
    out = Path(__file__).resolve().parents[1] / "sample_payload.json"
    out.write_text(json.dumps(sample, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Sample payload written to: {out}")


if __name__ == "__main__":
    main()
