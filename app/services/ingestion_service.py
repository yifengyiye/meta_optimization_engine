from app.schemas.input_models import AnalyzeRequest


class IngestionService:
    def load_request(self, payload: AnalyzeRequest) -> list:
        return payload.records

