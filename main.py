import asyncio
import logging
import os
import shutil
import stat

from bot_start import dp, bot
from handlers.register_handlers import register_handlers
from src.config import conf
from utils.middlewares.album_md import AlbumMiddleware


async def start_bot():
    await register_handlers(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    dp.message.middleware(AlbumMiddleware())
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    try:
        logging.basicConfig(level=conf.logging_level)
        logging.getLogger('openai._base_client').disabled = True
        asyncio.run(start_bot())
    except (KeyboardInterrupt, SystemExit):
        logging.info('Bot stopped')
        shutil.rmtree('files')
