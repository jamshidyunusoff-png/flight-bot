"""
Central configuration — reads from environment variables / .env file.
"""

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    bot_token: str
    database_url: str = "flights.db"

    @property
    def db_path(self) -> str:
        return self.database_url


settings = Settings()  # type: ignore[call-arg]
