"""Application settings loaded from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # -- App --
    app_env: str = "development"
    app_debug: bool = True
    secret_key: str = "change-me-to-a-random-secret-key"

    # -- Database --
    database_url: str = "postgresql+asyncpg://adforge:adforge@postgres:5432/adforge"
    database_url_sync: str = "postgresql://adforge:adforge@postgres:5432/adforge"

    # -- Redis --
    redis_url: str = "redis://redis:6379/0"

    # -- Celery --
    celery_broker_url: str = "redis://redis:6379/1"
    celery_result_backend: str = "redis://redis:6379/2"

    # -- LLM --
    anthropic_api_key: str = ""
    openai_api_key: str = ""

    # -- Meta Ads --
    meta_app_id: str = ""
    meta_app_secret: str = ""
    meta_access_token: str = ""

    # -- Auth --
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24  # 24 hours

    model_config = {"env_file": ".env", "extra": "ignore"}

    @property
    def has_anthropic_key(self) -> bool:
        return bool(self.anthropic_api_key)

    @property
    def has_meta_credentials(self) -> bool:
        return bool(self.meta_app_id and self.meta_app_secret)


settings = Settings()
