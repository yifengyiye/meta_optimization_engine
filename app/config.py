from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Meta Optimization Engine"
    app_version: str = "0.1.0"
    rule_version: str = "2026-04-07"
    rules_path: Path = Path(__file__).resolve().parent / "rules" / "meta_rules.yaml"

    model_config = SettingsConfigDict(env_prefix="MOE_", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()

