
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()


class Settings(BaseSettings):
    app_name: str = "TruthLens AI"
    app_env: str = "development"
    database_path: str = "truthlens_history.db"

    # Optional AI provider configuration
    openai_api_key: str = ""
    openai_model: str = "gpt-4.1-mini"

    # Optional web search configuration
    tavily_api_key: str = ""

    # Application limits
    max_text_length: int = 15000
    request_timeout_seconds: int = 20
    demo_mode: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
