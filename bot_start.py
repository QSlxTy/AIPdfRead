import logging

from src.bot.dispatcher import get_dispatcher

from src.config import conf
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot


bot = Bot(token=conf.bot.token, parse_mode='HTML')
storage = MemoryStorage()
logger = logging.getLogger(__name__)
dp = get_dispatcher(storage=storage)