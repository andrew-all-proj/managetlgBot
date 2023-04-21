from datetime import datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker

import config
from create_bot import bot, Keybords
from form_state import Form
from handlers.msg_delete import msg_delete


async def edit_events(msg, state, data):
    """
    Редактирование события
    """
    await msg_delete(bot, msg.from_user.id, data["data"].id_last_msg)
    await msg_delete(bot, msg.from_user.id, msg.message_id)
    session = sessionmaker(bind=engine)
    s = session()
    try:
        id_event = s.query(Events.id_event).filter(
            and_(Events.id_event == msg.text[1:], Events.completed == False)).one()
        data["data"].id_event = id_event
    except Exception as ex:
        send_info_msg = await bot.send_message(msg.from_user.id, "Нет такого события", reply_markup=Keybords.exit)
        data["data"].id_last_msg = send_info_msg.message_id
        return
    s.close()
    send_info_msg = await bot.send_message(msg.from_user.id, "Выберете действие", reply_markup=Keybords.edit_events_key)
    data["data"].id_last_msg = send_info_msg.message_id
    await Form.choose_action_event.set()
    await state.update_data(data)


async def choose_action_event(msg: types.Message, state: FSMContext):
    """
    Вызывает главное меню на любое сообщение
    """
    data = await state.get_data()
    await msg_delete(bot, msg.from_user.id, msg.message_id)
    await msg_delete(bot, msg.from_user.id, data["data"].id_last_msg)
    session = sessionmaker(bind=engine)
    s = session()
    if msg.text.lower() == 'посмотреть':
        event = s.query(Events).filter(and_(Events.id_event == data["data"].id_event[0])).one()
        media = s.query(MediaContens).filter(MediaContens.id_media == event.id_media).one()
        type_media = s.query(TypeMedia).filter(TypeMedia.id_type_media == media.id_type_media).one()
        with open(f'{config.PATH_FOR_MEDIA}/{type_media.type_media}/{media.local_path}', "rb") as f:
            file_send = f.read()
        if type_media.type_media == 'video':
            send_info_msg = await bot.send_video(msg.from_user.id, video=file_send,
                                                 caption=f"id:/{event.id_event}\n"
                                                         f"date start: {event.date_start}\n"
                                                         f"date stop: {event.date_stop}",
                                                 reply_markup=Keybords.main_meny)
        else:
            send_info_msg = await bot.send_photo(msg.from_user.id, photo=file_send,
                                                 caption=f"id:/{event.id_event}\n"
                                                         f"date start: {event.date_start}\n"
                                                         f"date stop: {event.date_stop}",
                                                 reply_markup=Keybords.exit)
        data["data"].id_last_msg = send_info_msg.message_id
        await state.update_data(data)
        await Form.main_meny.set()
    elif msg.text.lower() == 'удалить':
        send_info_msg = await bot.send_message(msg.from_user.id, f"Удалить /{data['data'].id_event[0]}?",
                                               reply_markup=Keybords.key_yes_no)
        data["data"].id_last_msg = send_info_msg.message_id
        await Form.delete_event.set()
        await state.update_data(data)


async def delete_event(msg: types.Message, state: FSMContext):
    """
    Удаление события
    Подумать!!! удалять опублекованное событие или нет
    """
    data = await state.get_data()
    await msg_delete(bot, msg.from_user.id, data["data"].id_last_msg)
    await msg_delete(bot, msg.from_user.id, msg.message_id)
    session = sessionmaker(bind=engine)
    s = session()
    event = s.query(Events).filter(Events.id_event == data["data"].id_event[0]).one()
    event.date_stop = datetime.now()
    event.id_message = -1
    s.commit()
    s.close()
    send_info_msg = await bot.send_message(msg.from_user.id, "Удалено",
                                           reply_markup=Keybords.main_meny)
    data["data"].id_last_msg = send_info_msg.message_id
    await Form.main.set()
    await state.update_data(data)


def register_handler_edit_events(dp: Dispatcher):
    dp.register_message_handler(choose_action_event, lambda message: message.text in ["Посмотреть", "Удалить"],
                                state=Form.choose_action_event)
    dp.register_message_handler(delete_event, lambda message: message.text in ["Да", "да"],
                                state=Form.delete_event)
