from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "myapp"
    app_debug: bool = False
    app_version: str = "0.0.1"

    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str
    # db_url: str


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"


@lru_cache()
def get_settings():
    return Settings()