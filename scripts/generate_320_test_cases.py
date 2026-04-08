import csv
import json
import re
from copy import deepcopy
from pathlib import Path


ROOT = Path(r"D:\agent\meta_agent")
TABLE_PATH = ROOT / "meta_ads_metrics_threshold_actions_table.md"
OUT_DIR = ROOT / "meta_optimization_engine" / "test_data"
JSON_PATH = OUT_DIR / "meta_ads_320_test_cases.json"
CSV_PATH = OUT_DIR / "meta_ads_320_test_cases_summary.csv"


def safe_div(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def base_record(case_id: int) -> dict:
    return {
        "date": "2026-04-07",
        "account_id": "acc_test_001",
        "campaign_id": f"camp_{case_id:03d}",
        "adset_id": f"adset_{case_id:03d}",
        "ad_id": f"ad_{case_id:03d}",
        "campaign_name": "Meta Engine Test Campaign",
        "adset_name": f"Test Adset {case_id}",
        "ad_name": f"Test Ad {case_id}",
        "spend": 120.0,
        "impressions": 10000,
        "reach": 5000,
        "frequency": 2.0,
        "clicks": 120,
        "link_clicks": 95,
        "outbound_clicks": 85,
        "landing_page_views": 75,
        "add_to_cart": 0,
        "initiate_checkout": 0,
        "purchases": 0,
        "revenue": 0.0,
        "average_order_value": 0.0,
        "objective": "purchase",
        "placement": "feed",
        "country": "US",
        "audience_type": "broad",
        "is_retargeting": False,
        "comments": 2,
        "shares": 1,
        "saves": 1,
        "video_3s_views": 0,
        "video_50p_views": 0,
        "video_95p_views": 0,
        "historical_ctr_avg": 0.015,
        "historical_cpa_avg": 60.0,
        "historical_roas_avg": 1.5,
        "refund_rate": 0.02,
    }


def recalc(record: dict) -> dict:
    record = deepcopy(record)
    record["frequency"] = round(safe_div(record["impressions"], record["reach"]), 4) if record.get("reach") else record.get("frequency", 0)
    record["average_order_value"] = round(safe_div(record["revenue"], record["purchases"]), 4) if record.get("purchases") else 0.0
    return record


def apply_metric_rules(metric_text: str, record: dict) -> dict:
    text = metric_text
    r = deepcopy(record)

    if "CTR < 0.5%" in text:
        r["impressions"] = 10000
        r["clicks"] = 40
        r["link_clicks"] = 30
    elif "CTR 0.5% - 0.8%" in text:
        r["impressions"] = 10000
        r["clicks"] = 65
        r["link_clicks"] = 50
    elif "CTR 0.8% - 1.0%" in text:
        r["impressions"] = 10000
        r["clicks"] = 90
        r["link_clicks"] = 70
    elif "CTR 1.0% - 1.5%" in text:
        r["impressions"] = 10000
        r["clicks"] = 120
        r["link_clicks"] = 95
    elif "CTR 1.5% - 2.5%" in text:
        r["impressions"] = 10000
        r["clicks"] = 180
        r["link_clicks"] = 140
    elif "CTR > 2.5%" in text:
        r["impressions"] = 10000
        r["clicks"] = 280
        r["link_clicks"] = 230

    if "Link CTR < 0.5%" in text:
        r["impressions"] = 10000
        r["link_clicks"] = 40
        r["clicks"] = max(r["clicks"], 60)
    elif "Link CTR 0.5% - 0.8%" in text:
        r["impressions"] = 10000
        r["link_clicks"] = 65
    elif "Link CTR 0.8% - 1.2%" in text:
        r["impressions"] = 10000
        r["link_clicks"] = 100
    elif "Link CTR 1.2% - 2.0%" in text:
        r["impressions"] = 10000
        r["link_clicks"] = 150

    if "CTR 高 + Link CTR 低" in text:
        r["impressions"] = 10000
        r["clicks"] = 230
        r["link_clicks"] = 40
    if "CTR 低 + CPC 高" in text:
        r["impressions"] = 10000
        r["clicks"] = 50
        r["spend"] = 320.0
        r["link_clicks"] = 35
    if "CTR 正常 + CPC 高" in text:
        r["impressions"] = 10000
        r["clicks"] = 120
        r["spend"] = 700.0
        r["link_clicks"] = 95
    if "CTR 高 + CPC 低" in text:
        r["impressions"] = 10000
        r["clicks"] = 250
        r["spend"] = 80.0
        r["link_clicks"] = 210

    if "CPM 比近 7 天均值高 20% 以内" in text:
        r["spend"] = 110.0
        r["impressions"] = 10000
    elif "CPM 比近 7 天均值高 20% - 40%" in text:
        r["spend"] = 240.0
        r["impressions"] = 10000
    elif "CPM 比近 7 天均值高 40% 以上" in text:
        r["spend"] = 320.0
        r["impressions"] = 10000
    if "CPM 高 + Frequency 高" in text:
        r["spend"] = 260.0
        r["impressions"] = 10000
        r["reach"] = 1800
    if "CPM 高 + Frequency 不高" in text:
        r["spend"] = 260.0
        r["impressions"] = 10000
        r["reach"] = 6500

    if "拉新 `Frequency > 3`" in text or "Frequency > 3" in text and "拉新" in text:
        r["is_retargeting"] = False
        r["reach"] = 2500
        r["impressions"] = 10000
    if "拉新 `Frequency > 4`" in text or "Frequency > 4" in text:
        r["is_retargeting"] = False
        r["reach"] = 2000
        r["impressions"] = 10000
        r["clicks"] = 70
    if "再营销 `Frequency > 6`" in text:
        r["is_retargeting"] = True
        r["audience_type"] = "retargeting"
        r["reach"] = 1200
        r["impressions"] = 9000
    if "`Frequency 高` 但 `CTR` 还稳" in text:
        r["reach"] = 2500
        r["impressions"] = 10000
        r["clicks"] = 130

    if "LPV / Click < 60%" in text:
        r["link_clicks"] = 180
        r["landing_page_views"] = 80
        r["clicks"] = max(r["clicks"], 180)
    elif "LPV / Click 60% - 70%" in text:
        r["link_clicks"] = 150
        r["landing_page_views"] = 95
    elif "LPV / Click 70% - 85%" in text:
        r["link_clicks"] = 150
        r["landing_page_views"] = 115
    elif "LPV / Click > 85%" in text:
        r["link_clicks"] = 150
        r["landing_page_views"] = 135

    if "CTR 高 + LPV 低" in text:
        r["impressions"] = 10000
        r["clicks"] = 220
        r["link_clicks"] = 180
        r["landing_page_views"] = 70
    if "LPV 正常 + AddToCart / LPV < 3%" in text:
        r["link_clicks"] = 150
        r["landing_page_views"] = 120
        r["add_to_cart"] = 2
    elif "AddToCart / LPV 3% - 5%" in text:
        r["landing_page_views"] = 120
        r["add_to_cart"] = 5
    elif "AddToCart / LPV 5% - 8%" in text:
        r["landing_page_views"] = 120
        r["add_to_cart"] = 8
    elif "AddToCart / LPV > 8%" in text:
        r["landing_page_views"] = 120
        r["add_to_cart"] = 12

    if "评论区频繁问价格" in text:
        r["comments"] = 22
        r["add_to_cart"] = min(r["add_to_cart"], 3)
    if "评论区频繁问真假/效果" in text:
        r["comments"] = 25
        r["add_to_cart"] = min(r["add_to_cart"], 3)

    if "InitiateCheckout / ATC < 20%" in text:
        r["add_to_cart"] = max(r["add_to_cart"], 15)
        r["initiate_checkout"] = 2
    elif "InitiateCheckout / ATC 20% - 30%" in text:
        r["add_to_cart"] = max(r["add_to_cart"], 15)
        r["initiate_checkout"] = 4
    elif "InitiateCheckout / ATC 30% - 45%" in text:
        r["add_to_cart"] = max(r["add_to_cart"], 15)
        r["initiate_checkout"] = 6
    elif "InitiateCheckout / ATC > 45%" in text:
        r["add_to_cart"] = max(r["add_to_cart"], 15)
        r["initiate_checkout"] = 8

    if "AddToCart 高 + InitiateCheckout 低" in text:
        r["add_to_cart"] = 16
        r["initiate_checkout"] = 2
    if "InitiateCheckout 高 + Purchase 低" in text:
        r["initiate_checkout"] = 10
        r["purchases"] = 0
        r["revenue"] = 0.0

    if "Purchase / LPV < 0.5%" in text:
        r["landing_page_views"] = max(r["landing_page_views"], 200)
        r["purchases"] = 0
        r["revenue"] = 0.0
    elif "Purchase / LPV 0.5% - 1%" in text:
        r["landing_page_views"] = max(r["landing_page_views"], 200)
        r["purchases"] = 1
        r["revenue"] = 80.0
    elif "Purchase / LPV 1% - 3%" in text:
        r["landing_page_views"] = max(r["landing_page_views"], 150)
        r["purchases"] = 3
        r["revenue"] = 240.0
    elif "Purchase / LPV > 3%" in text:
        r["landing_page_views"] = max(r["landing_page_views"], 100)
        r["purchases"] = 5
        r["revenue"] = 500.0

    if "CPA <= 目标值" in text:
        r["spend"] = 120.0
        r["purchases"] = 2
        r["revenue"] = 240.0
    elif "CPA = 目标值的 100% - 120%" in text:
        r["spend"] = 110.0
        r["purchases"] = 1
        r["revenue"] = 140.0
        r["historical_cpa_avg"] = 100.0
    elif "CPA = 目标值的 120% - 150%" in text:
        r["spend"] = 135.0
        r["purchases"] = 1
        r["revenue"] = 140.0
        r["historical_cpa_avg"] = 100.0
    elif "CPA > 目标值的 150%" in text or "CPA > 目标值 1.5 倍" in text:
        r["spend"] = 190.0
        r["purchases"] = 1
        r["revenue"] = 120.0
        r["historical_cpa_avg"] = 100.0

    if "CPA 高 + CTR 低" in text:
        r["spend"] = 250.0
        r["impressions"] = 10000
        r["clicks"] = 60
        r["link_clicks"] = 45
        r["purchases"] = 1
        r["revenue"] = 120.0
    if "CPA 高 + CTR 正常 + CVR 低" in text:
        r["spend"] = 220.0
        r["clicks"] = 180
        r["link_clicks"] = 150
        r["landing_page_views"] = 120
        r["purchases"] = 1
        r["revenue"] = 110.0
    if "CPA 高 + CTR 高 + CVR 正常" in text:
        r["spend"] = 260.0
        r["impressions"] = 10000
        r["clicks"] = 250
        r["link_clicks"] = 220
        r["landing_page_views"] = 150
        r["purchases"] = 2
        r["revenue"] = 220.0
    if "CPA 高 + AOV 低" in text:
        r["spend"] = 200.0
        r["purchases"] = 2
        r["revenue"] = 120.0
        r["average_order_value"] = 60.0

    if "ROAS 高于盈亏平衡线 20% 以上" in text:
        r["spend"] = 100.0
        r["revenue"] = 150.0
        r["purchases"] = 2
    elif "ROAS 接近平衡线" in text:
        r["spend"] = 120.0
        r["revenue"] = 120.0
        r["purchases"] = 2
    elif "ROAS 低于平衡线 10% - 20%" in text:
        r["spend"] = 120.0
        r["revenue"] = 102.0
        r["purchases"] = 2
    elif "ROAS 低于平衡线 20% 以上" in text or "ROAS < 平衡线" in text:
        r["spend"] = 120.0
        r["revenue"] = 80.0
        r["purchases"] = 1

    if "ROAS 下降但 CPA 没明显变差" in text:
        r["spend"] = 120.0
        r["purchases"] = 2
        r["revenue"] = 100.0
        r["average_order_value"] = 50.0
    if "订单量增加但利润没增加" in text:
        r["spend"] = 200.0
        r["purchases"] = 6
        r["revenue"] = 210.0
        r["average_order_value"] = 35.0
    if "AOV 持续低于账户均值" in text:
        r["average_order_value"] = 55.0
        r["purchases"] = 3
        r["revenue"] = 165.0

    if "视频 `前 3 秒留存低`" in text:
        r["video_3s_views"] = 800
        r["impressions"] = 10000
        r["clicks"] = 80
    if "视频 `前 3 秒好 + 点击低`" in text:
        r["video_3s_views"] = 3500
        r["impressions"] = 10000
        r["clicks"] = 70
    if "评论区大量问价格" in text:
        r["comments"] = 30
    if "评论区大量质疑真假" in text:
        r["comments"] = 30
    if "评论区跑偏严重" in text:
        r["comments"] = 40

    if "Ads Manager 数据变差，但后台订单没明显变差" in text:
        r["spend"] = 150.0
        r["initiate_checkout"] = 8
        r["purchases"] = 0
        r["revenue"] = 120.0
    if "Purchase 事件突然归零" in text:
        r["purchases"] = 0
        r["initiate_checkout"] = 5
        r["revenue"] = 0.0
    if "某设备/浏览器转化突然消失" in text:
        r["country"] = "US"
        r["placement"] = "feed"
        r["purchases"] = 0
        r["initiate_checkout"] = 6

    if "广告赚钱但花不出去" in text:
        r["spend"] = 40.0
        r["impressions"] = 1500
        r["clicks"] = 35
        r["link_clicks"] = 30
        r["landing_page_views"] = 25
        r["add_to_cart"] = 4
        r["initiate_checkout"] = 3
        r["purchases"] = 1
        r["revenue"] = 90.0
    if "花费涨了但转化没同步增长" in text:
        r["spend"] = 320.0
        r["purchases"] = 2
        r["revenue"] = 180.0
    if "放量后 `Frequency` 快速升高" in text:
        r["reach"] = 2200
        r["impressions"] = 10000
    if "复制广告组后表现明显变差" in text:
        r["spend"] = 200.0
        r["purchases"] = 1
        r["revenue"] = 90.0
    if "单一素材贡献 70% 以上转化" in text:
        r["comments"] = 15
        r["purchases"] = 4
        r["revenue"] = 400.0
    if "拉新效果差，但再营销很好" in text:
        r["is_retargeting"] = False
        r["purchases"] = 0
        r["revenue"] = 0.0

    if "新素材上线时间短" in text:
        r["impressions"] = 1200
        r["clicks"] = 16
        r["link_clicks"] = 12
        r["spend"] = 18.0
        r["landing_page_views"] = 10
    if "页面刚改版" in text:
        r["landing_page_views"] = 90
        r["add_to_cart"] = 4
    if "大促预热期" in text:
        r["add_to_cart"] = 12
        r["initiate_checkout"] = 5
        r["purchases"] = 0

    if "Lead Ads" in text:
        r["objective"] = "lead"
        r["purchases"] = 0
        r["revenue"] = 0.0
        r["spend"] = 45.0
    if "咨询广告消息多但成交弱" in text:
        r["objective"] = "message"
        r["purchases"] = 0
        r["revenue"] = 0.0

    if "免邮后转化变好但利润变差" in text:
        r["spend"] = 140.0
        r["purchases"] = 3
        r["revenue"] = 130.0
        r["average_order_value"] = 43.33
    if "折扣活动后低质量订单变多" in text:
        r["spend"] = 130.0
        r["purchases"] = 4
        r["revenue"] = 120.0
        r["average_order_value"] = 30.0

    if "某版位 `CTR` 明显低于其他版位" in text:
        r["placement"] = "stories"
        r["clicks"] = 60
    if "Reels 点击好、Feed 转化好" in text:
        r["placement"] = "reels"
        r["clicks"] = 240
        r["link_clicks"] = 180
    if "同一广告多次频繁编辑后数据变差" in text:
        r["clicks"] = 90
        r["purchases"] = 1
        r["revenue"] = 80.0

    if "DPA" in text or "目录广告" in text:
        r["placement"] = "feed"
        r["link_clicks"] = 180
    if "再营销" in text:
        r["is_retargeting"] = True
        r["audience_type"] = "retargeting"
    if "新客" in text:
        r["is_retargeting"] = False
        r["audience_type"] = "new_customer"
    if "地区" in text or "市场" in text:
        r["country"] = "CA"
    if "Stories" in text:
        r["placement"] = "stories"
    if "Reels" in text:
        r["placement"] = "reels"
    if "Feed" in text:
        r["placement"] = "feed"

    if "Refund Rate" in text or "退款率" in text:
        r["refund_rate"] = 0.12

    return recalc(r)


def isolate_for_expected_action(record: dict, expected_action: str) -> dict:
    r = deepcopy(record)

    if expected_action in {"OPTIMIZE", "OBSERVE", "REPLACE_CREATIVE", "EXPAND_AUDIENCE", "SCALE_OR_BUDGET"}:
        r["add_to_cart"] = min(r["add_to_cart"], 1)
        r["initiate_checkout"] = min(r["initiate_checkout"], 0)
        r["purchases"] = 0
        r["revenue"] = 0.0
        r["average_order_value"] = 0.0

    if expected_action == "FIX_LANDING_PAGE":
        r["add_to_cart"] = min(r["add_to_cart"], 0)
        r["initiate_checkout"] = 0
        r["purchases"] = 0
        r["revenue"] = 0.0
        r["average_order_value"] = 0.0
        if r["link_clicks"] > 0:
            r["landing_page_views"] = min(r["landing_page_views"], max(int(r["link_clicks"] * 0.55), 1))

    if expected_action == "FIX_CHECKOUT":
        r["landing_page_views"] = max(r["landing_page_views"], 120)
        r["add_to_cart"] = max(r["add_to_cart"], 15)
        r["initiate_checkout"] = min(max(r["initiate_checkout"], 2), 4)
        r["purchases"] = 0
        r["revenue"] = 0.0
        r["average_order_value"] = 0.0

    if expected_action == "FIX_PAYMENT":
        r["landing_page_views"] = max(r["landing_page_views"], 120)
        r["add_to_cart"] = max(r["add_to_cart"], 15)
        r["initiate_checkout"] = max(r["initiate_checkout"], 8)
        r["purchases"] = 0
        r["revenue"] = 0.0
        r["average_order_value"] = 0.0

    if expected_action == "FIX_TRACKING":
        r["landing_page_views"] = max(r["landing_page_views"], 100)
        r["add_to_cart"] = max(r["add_to_cart"], 10)
        r["initiate_checkout"] = max(r["initiate_checkout"], 5)
        r["purchases"] = 0
        r["revenue"] = max(r["revenue"], 120.0)

    if expected_action == "PAUSE":
        r["purchases"] = min(r["purchases"], 1)
        r["revenue"] = min(r["revenue"], 60.0 if r["purchases"] else 0.0)
        r["average_order_value"] = 60.0 if r["purchases"] else 0.0

    return recalc(r)


def parse_rows() -> list[tuple[int, str, str]]:
    rows = []
    for line in TABLE_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        m = re.match(r"^\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|$", line)
        if not m:
            continue
        rows.append((int(m.group(1)), m.group(2), m.group(3)))
    rows.sort(key=lambda x: x[0])
    return rows


def expected_action_from_text(action_text: str) -> str:
    text = action_text
    if "直接停" in text or "直接关" in text or "应停" in text or "暂停" in text or "止损" in text:
        return "PAUSE"
    if "先查页面" in text or "修页面" in text or "落地页" in text or "商品页" in text:
        return "FIX_LANDING_PAGE"
    if "购物车" in text or "结账" in text:
        return "FIX_CHECKOUT"
    if "支付" in text:
        return "FIX_PAYMENT"
    if "像素" in text or "CAPI" in text or "归因" in text or "埋点" in text or "回传" in text:
        return "FIX_TRACKING"
    if "换素材" in text or "重做" in text or "创意" in text:
        return "REPLACE_CREATIVE"
    if "扩受众" in text or "扩人群" in text or "放宽受众" in text:
        return "EXPAND_AUDIENCE"
    if "提预算" in text or "扩量" in text:
        return "SCALE_OR_BUDGET"
    if "观察" in text:
        return "OBSERVE"
    return "OPTIMIZE"


def build_cases() -> list[dict]:
    cases = []
    for rule_no, metric_text, action_text in parse_rows():
        expected_action = expected_action_from_text(action_text)
        record = apply_metric_rules(metric_text, base_record(rule_no))
        record = isolate_for_expected_action(record, expected_action)
        cases.append(
            {
                "case_id": f"case_{rule_no:03d}",
                "source_rule_no": rule_no,
                "source_metric_text": metric_text,
                "expected_optimization_text": action_text,
                "expected_primary_action": expected_action,
                "record": record,
            }
        )
    return cases


def write_outputs(cases: list[dict]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps({"cases": cases}, ensure_ascii=False, indent=2), encoding="utf-8")

    with CSV_PATH.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "case_id",
                "source_rule_no",
                "source_metric_text",
                "expected_primary_action",
                "expected_optimization_text",
                "ad_id",
                "spend",
                "impressions",
                "clicks",
                "link_clicks",
                "landing_page_views",
                "add_to_cart",
                "initiate_checkout",
                "purchases",
                "revenue",
            ]
        )
        for case in cases:
            rec = case["record"]
            writer.writerow(
                [
                    case["case_id"],
                    case["source_rule_no"],
                    case["source_metric_text"],
                    case["expected_primary_action"],
                    case["expected_optimization_text"],
                    rec["ad_id"],
                    rec["spend"],
                    rec["impressions"],
                    rec["clicks"],
                    rec["link_clicks"],
                    rec["landing_page_views"],
                    rec["add_to_cart"],
                    rec["initiate_checkout"],
                    rec["purchases"],
                    rec["revenue"],
                ]
            )


def main():
    cases = build_cases()
    write_outputs(cases)
    print(f"Generated {len(cases)} cases")
    print(f"JSON: {JSON_PATH}")
    print(f"CSV:  {CSV_PATH}")


if __name__ == "__main__":
    main()
