from pydantic import BaseModel, Field


class Condition(BaseModel):
    field: str
    operator: str
    value: float | int | str | bool | list[float] | list[int] | list[str] | None = None


class Rule(BaseModel):
    id: str
    name: str
    enabled: bool = True
    level: str = "ad"
    category: str
    severity: str
    action_type: str
    conditions: list[Condition] = Field(default_factory=list)
    recommendation: str
    rationale: str = ""
    priority_score: int = 50
    tags: list[str] = Field(default_factory=list)

