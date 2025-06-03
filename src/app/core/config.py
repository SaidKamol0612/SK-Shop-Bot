import logging

from typing import Literal
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = (".env.temp", ".env")
LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class BotSettings(BaseModel):
    token: str


class LoggingConfig(BaseModel):
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str = LOG_DEFAULT_FORMAT
    log_date_format: str = LOG_DATE_FORMAT
    log_file: str = "bot.log"

    @property
    def log_level_value(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level.upper()]


class ApiSettings(BaseModel):
    base_url: str
    
    login: str
    password: str

    products_endpoint: str
    login_endpoint: str

    timeout: int = 30  # seconds

    def get_full_url(self, endpoint: str) -> str:
        return f"{self.base_url}/{endpoint.lstrip('/')}"

class GroupSettings(BaseModel):
    chat_id: str
    links : str

class DataBaseSettings(BaseModel):
    url: str
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP__",
    )

    bot: BotSettings
    logging: LoggingConfig = LoggingConfig()
    api: ApiSettings
    group: GroupSettings
    db: DataBaseSettings


settings = Settings()
