from app.schemas.rule_models import Condition, Rule


class RuleEngine:
    def _compare(self, actual, operator: str, expected) -> bool:
        if actual is None:
            return False
        if operator == "lt":
            return actual < expected
        if operator == "lte":
            return actual <= expected
        if operator == "gt":
            return actual > expected
        if operator == "gte":
            return actual >= expected
        if operator == "eq":
            return actual == expected
        if operator == "neq":
            return actual != expected
        if operator == "between":
            return expected[0] <= actual <= expected[1]
        if operator == "in":
            return actual in expected
        if operator == "not_in":
            return actual not in expected
        if operator == "is_true":
            return bool(actual) is True
        if operator == "is_false":
            return bool(actual) is False
        raise ValueError(f"Unsupported operator: {operator}")

    def matches(self, rule: Rule, context: dict) -> bool:
        for condition in rule.conditions:
            actual = context.get(condition.field)
            if not self._compare(actual, condition.operator, condition.value):
                return False
        return True

