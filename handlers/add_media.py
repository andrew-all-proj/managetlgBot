import logging
import os
from datetime import datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

import config
from create_bot import bot, Keybords
from form_state import Form
from handlers.auth_user import check_user
from handlers.msg_delete import msg_delete
from models.channels_model import ChannelModel
from models.init_bd import s
from models.media_contents_model import TypeMediaModel, MediaContentModel
from models.media_tags_model import TagModel


async def add_tag(msg: types.Message, state: FSMContext):
    """
    Добавление тегов для медиа
    """
    data = await state.get_data()
    await msg_delete(bot, msg.from_user.id, data["data"].id_last_msg)
    id_channel = s.query(ChannelModel.id_channel).filter(ChannelModel.name_channel == msg.text).first()
    tags = s.query(TagModel).filter(TagModel.id_channel == id_channel).all()
    tags_btn = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for tag in tags:
        tags_btn.row(tag.tag_name)
    tags_btn.row("Выход")
    send_info_msg = await bot.send_message(msg.from_user.id, "Выберите тег для медиа",
                                           reply_markup=tags_btn)
    data["data"].id_last_msg = send_info_msg.message_id
    await Form.save_tag.set()
    await state.update_data(data)


async def add_media_db(msg: types.Message, state: FSMContext):
    """
    Добавление медиа в БД
    Переделать добаляемое сообщение!!!
    """
    data = await state.get_data()
    await msg_delete(bot, msg.from_user.id, data["data"].id_last_msg)
    await msg_delete(bot, msg.from_user.id, msg.message_id)
    type_file = data["data"].last_msg.content_type
    if type_file == 'photo':
        id_file = data["data"].last_msg.photo[-1].file_id
    else:
        id_file = data["data"].last_msg[type_file]["file_id"]
    file = await bot.get_file(id_file)
    file_path = file.file_path
    root, ext = os.path.splitext(file_path[-6:])
    ext = ext.lower()
    try:
        data_type_media = s.query(TypeMediaModel).filter(TypeMediaModel.extension == ext.strip('.')).one()
    except Exception as ex:
        logging.error(f"{ex}:{msg.from_user.id}:extension:{ext}")
        s.close()
        send_info_msg = await bot.send_message(msg.from_user.id, f"Неизвестный формат файла\n"
                                                                 f"Отправте в бот медиа без сжатия как документ",
                                               reply_markup=Keybords.exit)
        data["data"].id_last_msg = send_info_msg.message_id
        await Form.time_post.set()
        return
    id_user = check_user(msg.from_user.id)
    if (data_type_media.type_media == 'audio'):
        gen_name = f"{root}.{data_type_media.extension}"
    else:
        suffix_name = datetime.now().strftime("%y%m%d_%H%M%S")
        gen_name = f"{data_type_media.type_media}_{suffix_name}.{data_type_media.extension}"
    destination = f"{config.CONTENT_DIR}/{id_user}/{data_type_media.name_dir}/{gen_name}"
    await bot.download_file(file_path, destination)
    try:
        media_contents = MediaContentModel(id_type_media=data_type_media.id_type_media,
                                      name_file=f'{gen_name}',
                                      id_user=id_user)
        s.add(media_contents)
        s.commit()
        id_media = media_contents.id_media
    except Exception as ex:
        logging.error(f"{ex}:{msg.from_user.id}:id_chat:{msg.from_user.id}")
        s.close()
        await bot.send_message(msg.from_user.id, f"Ошибка добавления в БД",
                               reply_markup=Keybords.main_meny)
        return
    channels = s.query(ChannelModel.name_channel).filter(ChannelModel.id_user_admin == id_user).all()
    s.close()
    channels_btn = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for channel in channels:
        channels_btn.row(channel.name_channel)
    channels_btn.row("Выход")
    send_info_msg = await bot.send_message(msg.from_user.id,
                                           "Файл сохранен. Добавить теги? Выберите канал или нажмите выход",
                                           reply_markup=channels_btn)
    s.close()
    data["data"].id_media = id_media
    data["data"].id_last_msg = send_info_msg.message_id
    await Form.add_tag.set()
    await state.update_data(data)


async def save_tag_for_media(msg, state: FSMContext):
    """
    Добавление медиа в канал
    """
    data = await state.get_data()
    try:
        id_tag = s.query(TagModel).filter(TagModel.tag_name == msg.text).one()
        media = s.query(MediaContentModel).filter(MediaContentModel.id_media == data["data"].id_media).one()
        media.tags.append(id_tag)
        s.commit()
    except Exception as ex:
        logging.error(f"{ex}: Ошибка привязки тега")
        s.close()
        await bot.send_message(msg.from_user.id, f"Ошибка привязки тега",
                               reply_markup=Keybords.main_meny)
    s.close()
    await bot.delete_message(msg.from_user.id, (data["data"].id_last_msg))
    await Form.add_media_db.set()
    await state.update_data(data)


async def msg_add_media(msg: types.Message, state: FSMContext):
    """
    Отправка информационого сообщения
    """
    data = await state.get_data()
    await bot.delete_message(msg.from_user.id, (data["data"].id_last_msg))
    await bot.delete_message(msg.from_user.id, msg.message_id)
    send_info_msg = await bot.send_message(msg.from_user.id, "Отправте в бот медиа без сжатия как документ",
                                           reply_markup=Keybords.exit)
    data["data"].id_last_msg = send_info_msg.message_id
    await Form.add_media.set()
    await state.update_data(data)


def register_handler_add_media(dp: Dispatcher):
    dp.register_message_handler(add_tag, lambda message: message.text not in ["Выход"], state=Form.add_tag)
    dp.register_message_handler(add_media_db, lambda message: message.text in ["да", "Да", "ДА"],
                                state=Form.add_media_db)
    dp.register_message_handler(save_tag_for_media, lambda message: message.text not in ["Выход"],
                                content_types=types.ContentType.ANY, state=Form.save_tag)
    dp.register_message_handler(msg_add_media, lambda message: message.text in ["Добавить медиа"],
                                state=Form.select_chanel)
