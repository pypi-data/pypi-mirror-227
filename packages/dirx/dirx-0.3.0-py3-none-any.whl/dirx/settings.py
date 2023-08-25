from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    monitored_directories: list[Path] = Field(default=[])


settings = Settings()
