import logging
import os
from datetime import  datetime

import aiogram
from sqlalchemy import and_

from convert_video.convert_video import convert_video, MetaDataVideo
from create_bot import bot
from handlers.msg_delete import msg_delete
from models.channels_model import ChannelModel
from models.init_bd import s

from models.events_model import EventModel
from models.media_contents_model import MediaContentModel
from models.posts_model import PostsModel
from config import Config, BASE_DIR

from aiogram import types



async def delete_post():
    events_list = s.query(EventModel).filter(and_(EventModel.completed == False,
                                                  EventModel.date_stop < datetime.now())).all()
    for event in events_list:
        logging.info(f"delete: {event.id_event}")
        channel = s.query(ChannelModel).filter(ChannelModel.id_channel == event.id_channel).first()
        if not channel:
            logging.info(f'channel not found id: {event.id_channel}')
            continue
        logging.info(f'id telegram: {channel.id_telegram}')
        logging.info(f'id message: {event.id_message}')
        await msg_delete(bot, channel.id_telegram, event.id_message)
        event.completed = True
        event.save()


class AddText:  # I can add text only first media
    def __init__(self, text):
        self.text = text
        self.ch = False

    def add_text(self):
        if not self.ch:
            self.ch = True
            return self.text
        return ''

async def last_used_media(list_media):
    for media in list_media:
        bd_data = s.query(MediaContentModel).get(media.id_media)
        bd_data.last_time_used = datetime.now()
        bd_data.save()


async def send_post():

    events_list = s.query(EventModel).filter(and_(EventModel.published == False,
                                                  EventModel.date_start < datetime.now())).all()
    for event in events_list:
        logging.info(f"id event: {event.id_event}")
        channel = s.query(ChannelModel).filter(ChannelModel.id_channel == event.id_channel).first()
        if not channel:
            logging.info(f'channel not found id: {event.id_channel}')
            continue
        post = s.query(PostsModel).filter(and_(PostsModel.id_post == event.id_post, PostsModel.is_archive == False)).first()
        if not post:
            logging.info(f'post not found id: {event.id_post}')
            continue
        text = AddText(f"{post.text}")
        if post.media:
            media_group = types.MediaGroup()
            for media in post.media:
                logging.info(f"send media id: {media.id_media}")
                path_to_file = f"{Config.PATH_FOR_MEDIA}/{media.id_user}/{media.type_media.type_media}/{media.name_file}"
                if media.type_media.type_media == 'video':
                    logging.info(f"send video: {path_to_file}")
                    media_group.attach_video(types.InputFile(path_to_file), caption=text.add_text(), parse_mode='HTML')
                elif media.type_media.type_media == 'image':
                    logging.info(f"send image: {path_to_file}")
                    media_group.attach_photo(types.InputFile(path_to_file),  caption=text.add_text(), parse_mode='HTML')
                elif media.type_media.type_media == 'audio':
                    media_group.attach_audio(types.InputFile(path_to_file), caption=text.add_text(), parse_mode='HTML')
                elif media.type_media.type_media == 'document':
                    media_group.attach_document(types.InputFile(path_to_file), caption=text.add_text(), parse_mode='HTML')
                else:
                    logging.info("file is not supported")
            try:
                logging.info(f"send msg start media group: {media_group}")
                send_info_msg = await bot.send_media_group(channel.id_telegram,
                                                           media=media_group)
                logging.info(f"send msg: {send_info_msg}")
                id_msg = send_info_msg[0].message_id
                await last_used_media(post.media)
            except aiogram.utils.exceptions.NetworkError as ex:
                if str(ex) == 'File too large for uploading. Check telegram api limits https://core.telegram.org/bots/api#senddocument':
                    logging.info(f"convert video: {path_to_file}")
                    meta_data = MetaDataVideo(path_to_file)
                    size_file = meta_data.file_size
                    bitrate = meta_data.bit_rate
                    logging.info(f"convert video size_file: {size_file}")
                    await convert_video(size_file, bitrate, path_to_file)
                    continue
            except Exception as ex:
                logging.info(f"Error send post with group media: {ex}")
                continue
        else:
            try:
                send_info_msg = await bot.send_message(channel.id_telegram,
                                                   text=f"{text.add_text()}",
                                                   parse_mode='HTML')
                id_msg = send_info_msg.message_id
            except Exception as ex:
                logging.info(f"Error send text post: {ex}")
                continue
        event.id_message = id_msg
        event.published = True
        event.save()




async def events():
    await send_post()
    await delete_post()
