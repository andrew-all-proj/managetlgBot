import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from sqlalchemy.orm import sessionmaker

from create_bot import bot, Form_data, Keybords
from form_state import Form
from handlers.auth_user import check_user
from handlers.msg_delete import msg_delete
from models.channels_model import ChannelModel
from models.init_bd import s


async def check_chanel(msg: types.Message, state: FSMContext):
    """
    Работа с выбраным каналом(чатом)
    """
    data = await state.get_data()
    await msg_delete(bot, msg.from_user.id, data["data"].id_last_msg)
    try:
        info_chanel = s.query(ChannelModel).filter(ChannelModel.name_channel == msg.text.strip()).one()
        data["data"].info_chanel = info_chanel
        s.close()
    except Exception as ex:
        s.close()
        logging.error(f"{ex}:{msg.from_user.id}:id_chat:{msg.from_user.id}")
        await Form.main.set()
        send_info_msg = await bot.send_message(msg.from_user.id, "Нет такого канала", reply_markup=Keybords.main_meny)
        data["data"].id_last_msg = send_info_msg.message_id
        return
    send_info_msg = await bot.send_message(msg.from_user.id, "Выберите действие", reply_markup=Keybords.chanel_meny)
    data["data"].id_last_msg = send_info_msg.message_id
    await Form.main.set() # await Form.select_chanel.set() !!!!!!!!!!!!!!!!!!!!!!!!
    await state.update_data(data)


# @dp.message_handler(lambda message: message.text in ["Список каналов"], state=Form.main_meny)
async def send_list_chanel(msg: types.Message, state: FSMContext):
    """
    Выводит список каналов
    """
    if not check_user(msg.from_user.id):
        await bot.send_message(msg.from_user.id,
                               f"Вы не авторизованы добавьте свой ID: {msg.from_user.id} на сайте: managetlg.com "
                               f"в меню настройки",
                               reply_markup=Keybords.main_meny)
        return
    data = await state.get_data()
    await msg_delete(bot, msg.from_user.id, data["data"].id_last_msg)
    await msg_delete(bot, msg.from_user.id, msg.message_id)
    id_user = check_user(msg.from_user.id)
    chanels = s.query(ChannelModel.name_channel).filter(ChannelModel.id_user_admin == id_user).all()
    s.close()
    chanels_btn = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for chanel in chanels:
        chanels_btn.row(chanel.name_channel)
    chanels_btn.row("Выход")
    send_info_msg = await bot.send_message(msg.from_user.id, "Выберите канал", reply_markup=chanels_btn)
    data["data"].id_last_msg = send_info_msg.message_id
    await Form.chanel.set()
    await state.update_data(data)


async def list_events(msg: types.Message, state: FSMContext):
    """
    Выводит список событий
    """
    data = await state.get_data()
    await msg_delete(bot, msg.from_user.id, data["data"].id_last_msg)
    await msg_delete(bot, msg.from_user.id, msg.message_id)
    session = sessionmaker(bind=engine)
    s = session()
    events = s.query(Events).filter(Events.completed == False).order_by(Events.date_start).all()
    s.close()
    for event in events:
        await bot.send_message(msg.from_user.id, f"id: /{event.id_event}\n"
                                                 f"start: {event.date_start}\n"
                                                 f"stop: {event.date_stop}", reply_markup=Keybords.exit)
    send_info_msg = await bot.send_message(msg.from_user.id, "Выберите действие", reply_markup=Keybords.chanel_meny)
    data["data"].id_last_msg = send_info_msg.message_id
    await Form.main.set()
    await state.update_data(data)



# @dp.message_handler(state='*')
async def cmd_start(msg, state: FSMContext):
    """
    Вызывает главное меню на любое сообщение
    Выводит ID канала при пересылке сообщения
    """
    data = {'data': Form_data}
    content_type = ['photo', 'video', "audio", "animation"]
    id_user = check_user(msg.from_user.id)
    if id_user:
        if msg.content_type in content_type:
            send_info_msg = await bot.send_message(msg.from_user.id, f"СОХРАНИТЬ ФАЙЛ?",
                                   reply_markup=Keybords.key_yes_no)
            data["data"].id_last_msg = send_info_msg.message_id
            data["data"].last_msg = msg
            await Form.add_media_db.set()
            await state.update_data(data)
            return


    #if msg.text[0] == '/' and msg.text[1:].isdigit():
        #await edit_events(msg, state, data)
        #return
    await msg_delete(bot, msg.from_user.id, msg.message_id)
    await msg_delete(bot, msg.from_user.id, data["data"].id_last_msg)
    send_info_msg = await bot.send_message(msg.from_user.id, "МЕНЮ", reply_markup=Keybords.main_meny)
    data["data"].id_last_msg = send_info_msg.message_id
    await state.update_data(data)
    await Form.main_meny.set()
    s.close()


def register_handler_main_meny(dp: Dispatcher):
    dp.register_message_handler(send_list_chanel, lambda message: message.text in ["Список каналов"],
                                state=Form.main_meny)
    dp.register_message_handler(list_events, lambda message: message.text in ["Посмотреть очередь"],
                                state=Form.select_chanel)
    dp.register_message_handler(check_chanel, lambda message: message.text not in ["Выход", "выход"], state=Form.chanel)
    dp.register_message_handler(cmd_start, state='*',
                                content_types=types.ContentType.ANY)
#content_types=types.ContentType.ANY