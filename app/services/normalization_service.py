from app.schemas.input_models import AdRecord


class NormalizationService:
    def normalize_record(self, record: AdRecord) -> AdRecord:
        if record.frequency is None and record.reach and record.reach > 0:
            record.frequency = round(record.impressions / record.reach, 4)
        if record.average_order_value is None and record.purchases > 0:
            record.average_order_value = round(record.revenue / record.purchases, 4)
        return record

