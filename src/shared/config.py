import os
from enum import StrEnum

from pydantic_settings import BaseSettings


class ServerEnv(StrEnum):
    LOCAL = "local"
    DOCKER = "docker"


ENV = os.getenv("ENV", ServerEnv.LOCAL)
SERVER_PORT = os.getenv("PORT", "8000")


class LocalSettings(BaseSettings):
    db_url: str = "postgresql://chat:chat-pw@127.0.0.1:54320/chat"
    async_db_url: str = "postgresql+asyncpg://chat:chat-pw@127.0.0.1:54320/chat"
    app_secret_key: str = "cd3649c0545be584544ee9f4fa87050e8b7955796bfaecbb62c03c58593d904a"
    redis_host: str = "127.0.0.1"
    redis_port: int = 63790


class DockerSettings(BaseSettings):
    db_url: str = "postgresql://chat:chat-pw@db:5432/chat"
    async_db_url: str = "postgresql+asyncpg://chat:chat-pw@db:5432/chat"
    app_secret_key: str = "cd3649c0545be584544ee9f4fa87050e8b7955796bfaecbb62c03c58593d904a"
    redis_host: str = "redis"
    redis_port: int = 6379


def get_settings(env: ServerEnv):
    match env:
        case ServerEnv.DOCKER:
            return DockerSettings()
        case _:
            return LocalSettings()


settings = get_settings(env=ENV)
