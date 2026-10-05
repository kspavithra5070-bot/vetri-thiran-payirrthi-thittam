from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# Project root folder
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    app_name: str = "EduGenie"
    environment: str = "development"

    host: str = "127.0.0.1"
    port: int = 8000

    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.8-flash"

    local_model_name: str = "MBZUAI/LaMini-Flan-T5-783M"
    use_local_model: bool = False

    max_input_chars: int = 12000
    cors_origins: str = "*"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()