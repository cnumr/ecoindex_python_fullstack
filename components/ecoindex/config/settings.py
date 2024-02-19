from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    CORS_ALLOWED_CREDENTIALS: bool = True
    CORS_ALLOWED_HEADERS: list = ["*"]
    CORS_ALLOWED_METHODS: list = ["*"]
    CORS_ALLOWED_ORIGINS: list = ["*"]
    DAILY_LIMIT_PER_HOST: int = 0
    DATABASE_URL: str = "sqlite+aiosqlite:///db.sqlite3"
    DOCKER_CONTAINER: bool = False
    DEBUG: bool = False
    ENABLE_SCREENSHOT: bool = False
    EXCLUDED_HOSTS: list[str] = ["localhost", "127.0.0.1"]
    FRONTEND_BASE_URL: str = "https://www.ecoindex.fr"
    REDIS_CACHE_HOST: str = "localhost"
    SCREENSHOTS_GID: int | None = None
    SCREENSHOTS_UID: int | None = None
    TZ: str = "Europe/Paris"
    WAIT_AFTER_SCROLL: int = 3
    WAIT_BEFORE_SCROLL: int = 3
    model_config = SettingsConfigDict(env_file=".env")
