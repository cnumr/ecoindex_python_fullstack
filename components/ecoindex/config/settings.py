from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    CORS_ALLOWED_CREDENTIALS: bool = True
    CORS_ALLOWED_HEADERS: list = ["*"]
    CORS_ALLOWED_METHODS: list = ["*"]
    CORS_ALLOWED_ORIGINS: list = ["*"]
    DAILY_LIMIT_PER_HOST: int = 0
    DATABASE_URL: str = "sqlite+aiosqlite:///db.sqlite3"
    DEBUG: bool = True
    ENABLE_SCREENSHOT: bool = False
    REDIS_CACHE_HOST: str = "localhost"
    SCREENSHOTS_GID: int | None = None
    SCREENSHOTS_UID: int | None = None
    WAIT_AFTER_SCROLL: int = 3
    WAIT_BEFORE_SCROLL: int = 3
    WORKER_BACKEND_URL: str = "redis://localhost:6379/1"
    WORKER_BROKER_URL: str = "redis://localhost:6379/0"
    model_config = SettingsConfigDict(env_file=".env")
