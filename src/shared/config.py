from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = 'postgresql://fast-async:fast-async-pw@127.0.0.1:54320/fast-async'
    async_db_url: str = 'postgresql+asyncpg://fast-async:fast-async-pw@127.0.0.1:54320/fast-async'


settings = Settings()
