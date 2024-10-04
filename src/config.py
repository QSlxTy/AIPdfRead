import logging
from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv

load_dotenv()


@dataclass
class BotConfig:
    token: str = getenv('BOT_TOKEN')


@dataclass
class Tokens:
    openai = getenv('GPT_TOKEN')
    yandex = getenv('YADISK_TOKEN')


@dataclass
class Configuration:
    debug = bool(getenv('DEBUG'))
    logging_level = int(getenv('LOGGING_LEVEL', logging.INFO))
    bot = BotConfig()


conf = Configuration()
