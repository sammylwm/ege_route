import os

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


def get_env_file() -> bool:
    return os.getenv("APP_ENV", "dev") == "prod"


class ConfigBase(BaseSettings):
    env = "settings/"
    env += ".env" if get_env_file() else "dev.env"
    model_config = SettingsConfigDict(
        env_file=env, env_file_encoding="utf-8", extra="ignore"
    )


class BotConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="BOT_")
    TOKEN: SecretStr = SecretStr("")


class DatabaseConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="POSTGRES_")
    HOST: str = ""
    DB: str = ""
    USER: str = ""
    PASSWORD: SecretStr = SecretStr("")
    DB_URL: str = ""

    def __init__(self, **data):
        super().__init__(**data)
        self.DB_URL = (
            f"postgresql+asyncpg://{self.USER}:{self.PASSWORD.get_secret_value()}@{self.HOST}:"
            f"5432/{self.DB}"
        )

class Settings(BaseSettings):
    bot: BotConfig = BotConfig()
    db: DatabaseConfig = DatabaseConfig()

settings = Settings()