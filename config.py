from pathlib import Path
from typing import List

from aiogram.types import BotCommand
from pydantic import field_validator
from pydantic_settings import BaseSettings


class ProjConfig(BaseSettings):
    DATA_DIR: Path = Path(__file__).parent / 'data'

    class Config:
        env_prefix = 'PROJ_'
        env_file = '.env'
        extra = 'ignore'


class BotConfig(BaseSettings):
    TOKEN: str
    ADMINS: List[int] = []
    COMMANDS: List[BotCommand] = [
        BotCommand(
            command='start',
            description='Меню'
        )
    ]

    class Config:
        env_prefix = 'BOT_'
        env_file = '.env'
        extra = 'ignore'

    @field_validator('ADMINS', mode='before')
    def split_admins(cls, v):
        if isinstance(v, list):
            return v
        if not v:
            return []
        try:
            return [int(admin_id.strip()) for admin_id in str(v).split(',')]
        except Exception:
            raise ValueError('ADMINS value must be int,int,int')


class PostgresConfig(BaseSettings):
    NAME: str = "bot_db"
    HOST: str = "localhost"
    PORT: int = 5432
    PASSWORD: str = ""
    USER: str = "postgres"

    class Config:
        env_prefix = 'POSTGRES_'
        env_file = '.env'
        extra = 'ignore'

    @field_validator('PORT')
    def validate_port(cls, v):
        if not 1 <= v <= 65535:
            raise ValueError('Port must be between 1 and 65535')
        return v

    @property
    def URL(self) -> str:
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"


class ApiConfig(BaseSettings):
    TOKEN: str

    class Config:
        env_prefix = 'API_'
        env_file = '.env'
        extra = 'ignore'


class Config:
    psql: PostgresConfig = PostgresConfig()
    api: ApiConfig = ApiConfig()
    bot: BotConfig = BotConfig()
    proj: ProjConfig = ProjConfig()


cnf = Config()