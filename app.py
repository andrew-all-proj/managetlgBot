import asyncio
import logging
from logging.handlers import RotatingFileHandler

from aiogram.utils import executor

from config import Config, BASE_DIR
from create_bot import dp
from handlers.events_handler import events

rfh = RotatingFileHandler(
    filename=Config.PATH_LOG_FILE,
    mode='a',
    maxBytes=5*1024*1024,
    backupCount=2,
    encoding=None
)

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
                    datefmt='%H:%M:%S',
                    handlers=[
                        rfh
                   ]
                   )

async def on_startup(_):
    print("START ONLINE BOT")

from handlers import main_meny, add_media, add_new_channel, edit_events

add_media.register_handler_add_media(dp)
add_new_channel.register_handler_add_chanel(dp)
#edit_events.register_handler_edit_events(dp)
main_meny.register_handler_main_meny(dp)


async def scheduled(wait_for):
    """Запуск обработчика по рассписанию"""
    while True:
        await asyncio.sleep(wait_for)
        await events()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(5))  # через какой промежуток запускать в секундах
    logging.info("start bot")
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
