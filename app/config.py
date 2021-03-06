import json

from pydantic import BaseSettings, validator


class DB(BaseSettings):
    host: str
    port: int
    name: str
    user: str
    password: str


class Redis(BaseSettings):
    host: str
    db: int


class TgBot(BaseSettings):
    token: str
    admin_ids: list[int]
    use_redis: bool

    """@validator("admin_ids", pre=True, always=True)
    def admin_ids_list(cls, v) -> list[int]:
        return json.loads(v)"""


"""class Settings(BaseSettings):
    tg_bot: TgBot
    db: DB
    redis: Redis

    class Config:
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'"""


class SettingsExtractor(BaseSettings):
    # tg_bot
    TG_BOT__TOKEN: str
    TG_BOT__ADMIN_IDS: list[int]
    TG_BOT__USE_REDIS: bool

    # database
    DB__HOST: str
    DB__PORT: int
    DB__NAME: str
    DB__USER: str
    DB__PASSWORD: str

    # redis
    REDIS__HOST: str
    REDIS__DB: int


class Settings(BaseSettings):
    tg_bot: TgBot
    db: DB
    redis: Redis


def load_config() -> Settings:
    settings = SettingsExtractor()

    return Settings(
        tg_bot=TgBot(
            token=settings.TG_BOT__TOKEN,
            admin_ids=settings.TG_BOT__ADMIN_IDS,
            use_redis=settings.TG_BOT__USE_REDIS,
        ),
        db=DB(
            host=settings.DB__HOST,
            port=settings.DB__PORT,
            name=settings.DB__NAME,
            user=settings.DB__USER,
            password=settings.DB__PASSWORD,
        ),
        redis=Redis(host=settings.REDIS__HOST, db=settings.REDIS__DB),
    )
