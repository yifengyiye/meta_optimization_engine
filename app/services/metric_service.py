from app.schemas.input_models import AdRecord


def _safe_div(numerator: float, denominator: float) -> float | None:
    if not denominator:
        return None
    return numerator / denominator


def _round_metric(value: float | None, digits: int = 6) -> float | None:
    if value is None:
        return None
    return round(value, digits)


class MetricService:
    def _sample_size_ok(self, record: AdRecord) -> bool:
        target_cpa = record.historical_cpa_avg or 100.0
        spend_gate = target_cpa * 1.0
        click_gate = 30
        impression_gate = 1000

        if record.purchases > 0:
            return True
        if record.spend >= spend_gate and record.impressions >= impression_gate:
            return True
        if record.clicks >= click_gate and record.impressions >= impression_gate:
            return True
        return False

    def _creative_fatigue_risk(
        self,
        frequency: float | None,
        ctr: float | None,
        historical_ctr_avg: float | None,
        is_retargeting: bool,
    ) -> bool:
        if frequency is None:
            return False
        threshold = 6.0 if is_retargeting else 3.0
        if frequency <= threshold:
            return False
        if historical_ctr_avg is None or ctr is None:
            return True
        return ctr < historical_ctr_avg

    def _delivery_constrained(self, record: AdRecord, cpm: float | None) -> bool:
        if record.spend <= 0:
            return False
        if record.impressions < 500 and record.spend < 20:
            return True
        if cpm is not None and cpm > 0 and record.impressions < 1000 and record.spend > 0:
            return True
        return False

    def _data_anomaly_suspected(
        self,
        record: AdRecord,
        lpv_rate: float | None,
        purchase_cvr: float | None,
    ) -> bool:
        if record.spend > 100 and record.initiate_checkout > 0 and record.purchases == 0:
            return True
        if lpv_rate is not None and lpv_rate < 0.2 and record.link_clicks > 20:
            return True
        if purchase_cvr == 0 and record.revenue > 0:
            return True
        return False

    def compute_metrics(self, record: AdRecord) -> dict[str, float | bool | None]:
        ctr = _round_metric(_safe_div(record.clicks, record.impressions))
        link_ctr = _round_metric(_safe_div(record.link_clicks, record.impressions))
        outbound_ctr = _round_metric(_safe_div(record.outbound_clicks, record.impressions))
        cpc = _round_metric(_safe_div(record.spend, record.clicks), 4)
        cpm = _round_metric(_safe_div(record.spend * 1000, record.impressions), 4)
        lpv_rate = _round_metric(_safe_div(record.landing_page_views, record.link_clicks))
        add_to_cart_rate = _round_metric(_safe_div(record.add_to_cart, record.landing_page_views))
        checkout_rate = _round_metric(_safe_div(record.initiate_checkout, record.add_to_cart))
        purchase_cvr = _round_metric(_safe_div(record.purchases, record.landing_page_views))
        payment_success_rate = _round_metric(_safe_div(record.purchases, record.initiate_checkout))
        cpa = _round_metric(_safe_div(record.spend, record.purchases), 4)
        roas = _round_metric(_safe_div(record.revenue, record.spend), 4)
        aov = _round_metric(record.average_order_value or _safe_div(record.revenue, record.purchases), 4)
        save_rate = _round_metric(_safe_div(record.saves, record.impressions))
        share_rate = _round_metric(_safe_div(record.shares, record.impressions))
        comment_rate = _round_metric(_safe_div(record.comments, record.impressions))
        video_hook_rate = _round_metric(_safe_div(record.video_3s_views, record.impressions))
        video_mid_rate = _round_metric(_safe_div(record.video_50p_views, record.impressions))
        video_complete_rate = _round_metric(_safe_div(record.video_95p_views, record.impressions))

        historical_ctr_avg = record.historical_ctr_avg
        historical_cpa_avg = record.historical_cpa_avg
        historical_roas_avg = record.historical_roas_avg

        sample_size_ok = self._sample_size_ok(record)
        is_retargeting = record.is_retargeting
        creative_fatigue_risk = self._creative_fatigue_risk(
            record.frequency,
            ctr,
            historical_ctr_avg,
            is_retargeting,
        )
        delivery_constrained = self._delivery_constrained(record, cpm)
        data_anomaly_suspected = self._data_anomaly_suspected(record, lpv_rate, purchase_cvr)

        ctr_vs_history = (
            _round_metric(((ctr - historical_ctr_avg) / historical_ctr_avg), 4)
            if ctr is not None and historical_ctr_avg
            else None
        )
        cpa_vs_history = (
            _round_metric(((cpa - historical_cpa_avg) / historical_cpa_avg), 4)
            if cpa is not None and historical_cpa_avg
            else None
        )
        roas_vs_history = (
            _round_metric(((roas - historical_roas_avg) / historical_roas_avg), 4)
            if roas is not None and historical_roas_avg
            else None
        )

        return {
            "ctr": ctr,
            "link_ctr": link_ctr,
            "outbound_ctr": outbound_ctr,
            "cpc": cpc,
            "cpm": cpm,
            "lpv_rate": lpv_rate,
            "add_to_cart_rate": add_to_cart_rate,
            "checkout_rate": checkout_rate,
            "purchase_cvr": purchase_cvr,
            "payment_success_rate": payment_success_rate,
            "cpa": cpa,
            "roas": roas,
            "frequency": record.frequency,
            "aov": aov,
            "save_rate": save_rate,
            "share_rate": share_rate,
            "comment_rate": comment_rate,
            "video_hook_rate": video_hook_rate,
            "video_mid_rate": video_mid_rate,
            "video_complete_rate": video_complete_rate,
            "sample_size_ok": sample_size_ok,
            "is_retargeting": is_retargeting,
            "is_cold_traffic": not is_retargeting,
            "creative_fatigue_risk": creative_fatigue_risk,
            "delivery_constrained": delivery_constrained,
            "data_anomaly_suspected": data_anomaly_suspected,
            "ctr_vs_history": ctr_vs_history,
            "cpa_vs_history": cpa_vs_history,
            "roas_vs_history": roas_vs_history,
        }
