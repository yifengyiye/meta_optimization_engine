from app.rules.meta_rule_loader import RuleLoader
from app.services.rule_engine import RuleEngine


def test_rule_loader_loads_yaml():
    loader = RuleLoader("app/rules/meta_rules.yaml")
    rules = loader.load_rules()
    assert len(rules) >= 1


def test_rule_engine_matches_ctr_rule():
    loader = RuleLoader("app/rules/meta_rules.yaml")
    rules = loader.load_rules()
    rule = next(r for r in rules if r.id == "ctr_too_low_pause")
    engine = RuleEngine()
    context = {"ctr": 0.004, "sample_size_ok": True, "is_retargeting": False}
    assert engine.matches(rule, context) is True

