import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from create_bot import bot, Keybords
from form_state import Form
from handlers.msg_delete import msg_delete


# @dp.message_handler(lambda message: message.text in ["Добавить канал"], state=Form.main_meny)
async def add_channel_send_msg(msg: types.Message, state: FSMContext):
    """
    Для добавления нового канала надо переслать сообщение из добавляемого канала
    """
    data = await state.get_data()
    await msg_delete(bot, msg, data["data"].id_last_msg)
    await msg_delete(bot, msg, msg.message_id)
    send_info_msg = await bot.send_message(msg.from_user.id, "Перешлите сообщение из добавляемого канала",
                                           reply_markup=Keybords.exit)
    data["data"].id_last_msg = send_info_msg.message_id
    await Form.add_chanel.set()
    await state.update_data(data)


# @dp.message_handler(content_types=types.ContentType.ANY, state=Form.add_chanel)
async def add_chanel(msg, state: FSMContext):
    """
    Добавление нового канала
    Проверку сделать что бот добавлен в канал как админ
    """
    data = await state.get_data()
    await msg_delete(bot, msg, data["data"].id_last_msg)
    try:
        if msg["forward_from_chat"]["type"] == 'channel':
            await bot.send_message(msg.from_user.id, f"id: {msg['forward_from_chat']['id']}")
            await bot.send_message(msg.from_user.id, f"Название: {msg['forward_from_chat']['title']}")
            await bot.send_message(msg.from_user.id, f"Имя канала: @{msg['forward_from_chat']['username']}")
    except Exception as ex:
        logging.error(f"{ex}:{msg.from_user.id}:id_chat:{msg.from_user.id}")
        send_info_msg = await bot.send_message(msg.from_user.id, "Ошибка сообщения\n"
                                                                 "Перешлите сообщение из добавляемого канала",
                                               reply_markup=Keybords.exit)
        data["data"].id_last_msg = send_info_msg.message_id
        await Form.add_chanel.set()
        return
    data["data"].last_msg = msg
    send_info_msg = await bot.send_message(msg.from_user.id, "Добавить канал?", reply_markup=Keybords.key_yes_no)
    data["data"].id_last_msg = send_info_msg.message_id
    await Form.add_chanel_bd.set()
    await state.update_data(data)


# @dp.message_handler(lambda message: message.text in ["да", "Да", "ДА"], state=Form.add_chanel_bd)
async def add_chanel_in_db(msg: types.Message, state: FSMContext):
    """
    Сохранения канала в БД
    """
    data = await state.get_data()
    await msg_delete(bot, msg.from_user.id, data["data"].id_last_msg)
    """try:
        chanels = Chanels(link_chanel=data["data"].last_msg['forward_from_chat']['username'],
                          name_chanel=data["data"].last_msg['forward_from_chat']['title'],
                          id_telegram=data["data"].last_msg['forward_from_chat']['id'])
        chanels.save()
    except Events as ex:
        logging.info(f"{ex}:{msg.from_user.id}:id_chat:{msg.from_user.id}")
        send_info_msg = await bot.send_message(msg.from_user.id, "Ошибка сохранения", reply_markup=Keybords.exit)
        data["data"].id_last_msg = send_info_msg.message_id
        await Form.main.set()
        return
    send_info_msg = await bot.send_message(msg.from_user.id, "Канал сохранен", reply_markup=Keybords.exit)
    data["data"].id_last_msg = send_info_msg.message_id
    await state.update_data(data)"""
    await bot.send_message(msg.from_user.id, "Функция временно не работает добавте ID вручную на сайте", reply_markup=Keybords.exit)
    await Form.main.set()


def register_handler_add_chanel(dp: Dispatcher):
    dp.register_message_handler(add_channel_send_msg, lambda message: message.text in ["Добавить канал"],
                                state=Form.main_meny)
    dp.register_message_handler(add_chanel, lambda message: message.text not in ["Выход", "выход"],
                                content_types=types.ContentType.ANY, state=Form.add_chanel)
    dp.register_message_handler(add_chanel_in_db, lambda message: message.text in ["да", "Да", "ДА"],
                                state=Form.add_chanel_bd)
