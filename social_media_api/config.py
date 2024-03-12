from typing import Optional
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    ENV_STATE: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class GlobalConfig(BaseConfig):
    DATABASE_URL: Optional[str] = None
    DB_FORCE_ROLL_BACK: bool = False


class DevConfig(GlobalConfig):
    model_config = SettingsConfigDict(
        env_prefix="DEV_", env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class ProdConfig(GlobalConfig):
    model_config = SettingsConfigDict(
        env_prefix="PROD_", env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class TestConfig(GlobalConfig):
    model_config = SettingsConfigDict(
        env_prefix="TEST_", env_file=".env.test", env_file_encoding="utf-8", extra="ignore"
    )
    DATABASE_URL: Optional[str] = "sqlite:///test.db"
    DB_FORCE_ROLL_BACK: bool = True


@lru_cache()
def get_config(env_state: str):
    configs = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
    return configs[env_state]()


# Getting only "ENV_STATE" environment variable from .env file
config = get_config(BaseConfig().ENV_STATE)
