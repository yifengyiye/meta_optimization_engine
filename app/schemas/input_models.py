from pydantic import BaseModel, Field


class AdRecord(BaseModel):
    date: str
    account_id: str
    campaign_id: str
    adset_id: str
    ad_id: str
    campaign_name: str | None = None
    adset_name: str | None = None
    ad_name: str | None = None
    spend: float = 0.0
    impressions: int = 0
    reach: int | None = None
    frequency: float | None = None
    clicks: int = 0
    link_clicks: int = 0
    outbound_clicks: int = 0
    landing_page_views: int = 0
    add_to_cart: int = 0
    initiate_checkout: int = 0
    purchases: int = 0
    revenue: float = 0.0
    average_order_value: float | None = None
    objective: str | None = None
    placement: str | None = None
    country: str | None = None
    audience_type: str | None = None
    is_retargeting: bool = False
    comments: int = 0
    shares: int = 0
    saves: int = 0
    video_3s_views: int = 0
    video_50p_views: int = 0
    video_95p_views: int = 0
    historical_ctr_avg: float | None = None
    historical_cpa_avg: float | None = None
    historical_roas_avg: float | None = None


class AnalyzeRequest(BaseModel):
    records: list[AdRecord] = Field(default_factory=list)

