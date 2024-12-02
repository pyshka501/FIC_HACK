from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str
    admin_id: int
    bot_db: str



@dataclass
class Settings:
    bots: Bots


def get_settings(path: str) -> Settings:
    env = Env()
    env.read_env(path)
    return Settings(
        bots=Bots(
            bot_token=env.str("TOKEN"),
            admin_id=env.int("ADMIN_ID"),
            bot_db=env.str("DB_LITE"),
        )
    )

