from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

APP_PATH = Path(__file__).parent.resolve()


class ApplicationSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    db_uri: str = Field()
    pool_db: str = Field()


settings = ApplicationSettings()
