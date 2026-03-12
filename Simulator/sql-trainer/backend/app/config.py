from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    APP_TITLE: str = "SQL Trainer API"
    DEBUG: bool = False

    # Database (PostgreSQL)
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/sql_trainer"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8  # 8 hours

    # SQL Sandbox limits
    SANDBOX_TIMEOUT_SEC: int = 5
    SANDBOX_MAX_ROWS: int = 500

    class Config:
        env_file = ".env"


settings = Settings()
