import os
from pydantic_settings import BaseSettings, SettingsConfigDict

current_file_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_file_dir, ".env")


class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # The V2 way uses 'model_config' instead of 'class Config'
    model_config = SettingsConfigDict(env_file=env_path, env_file_encoding="utf-8")


settings = Settings()
