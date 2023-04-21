from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from token_ import token_

API_TOKEN = token_
bot = Bot(token=API_TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Keybords():
    key_yes_no = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key_yes_no.add('Да')
    key_yes_no.add('Нет')

    main_meny = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_meny.row('Список каналов', 'Добавить канал')

    chanel_meny = types.ReplyKeyboardMarkup(resize_keyboard=True)
    chanel_meny.add('Добавить медиа')
    chanel_meny.add('Посмотреть очередь')
    chanel_meny.add('Выход')

    edit_events_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
    edit_events_key.row('Посмотреть', 'Удалить')
    edit_events_key.add('Выход')

    exit = types.ReplyKeyboardMarkup(resize_keyboard=True)
    exit.row('Выход')

#insert
#one_time_keyboard=True одноразовая клавиатура


class Form_data:
    """
    Класс для структурированой передачи данных от одного хендлера к другому
    """
    id_last_msg = ''
    last_msg = ''
    info_chanel = ''
    id_media = ''
    id_event = ''
