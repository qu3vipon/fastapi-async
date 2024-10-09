from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = "postgresql://fast-async:fast-async-pw@127.0.0.1:54320/fast-async"
    async_db_url: str = "postgresql+asyncpg://fast-async:fast-async-pw@127.0.0.1:54320/fast-async"
    app_secret_key: str = "cd3649c0545be584544ee9f4fa87050e8b7955796bfaecbb62c03c58593d904a"


settings = Settings()
