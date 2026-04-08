from pathlib import Path

import yaml

from app.schemas.rule_models import Rule


class RuleLoader:
    def __init__(self, rules_path: Path):
        self.rules_path = Path(rules_path)

    def load_rules(self) -> list[Rule]:
        raw = yaml.safe_load(self.rules_path.read_text(encoding="utf-8")) or []
        return [Rule.model_validate(item) for item in raw]

