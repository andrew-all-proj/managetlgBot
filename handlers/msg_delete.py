import logging


async def msg_delete(bot, chat_id, id_msg):
    if id_msg == '' or id_msg == None:
        return True
    try:
        await bot.delete_message(chat_id, id_msg)
    except Exception as ex:
        logging.error(f"{ex}:{chat_id}:id_msg:{id_msg}")
        return False
