from pathlib import Path

from pydantic import AnyUrl, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    debug: bool = False
    database_url: AnyUrl = AnyUrl("sqlite:///lmmlis.sqlite3")
    secret_key: SecretStr = SecretStr("secret")
    cors_allowed_origins: list[str] = ["http://localhost:3000"]

    model_config = SettingsConfigDict(
        env_file=Path(".env"),
        extra="ignore",
    )


settings = Settings()
