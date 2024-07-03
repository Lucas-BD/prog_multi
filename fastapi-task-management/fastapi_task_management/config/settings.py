from pathlib import Path

from pydantic.v1 import BaseSettings

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_NAME: str
    DATABASE_TYPE: str

    class Config:
        env_file = f'{PROJECT_ROOT}/.env'


settings = Settings()