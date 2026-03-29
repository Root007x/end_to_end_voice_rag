from pydantic_settings import BaseSettings, SettingsConfigDict
import yaml
from box import Box


class Settings(BaseSettings):
    GROQ_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


setting = Settings()


class Config:
    def __init__(self):
        pass

    def load_yaml(self, file_path):
        with open(file_path, "r") as file:
            config = yaml.safe_load(file)
        return Box(config)


config = Config().load_yaml("config/config.yaml")
