"""Функция для тестового заполнения БД"""
import sys

from sqlalchemy.orm import sessionmaker
from pathlib import Path
path_proj = Path(__file__).resolve().parents[1]
sys.path.insert(1, str(path_proj))
from sheme_bd import engine, Users, MediaContens, Events, TypeMedia, Chanels

list_data = {
    "for": "add_data_in_bd",
    "data": [
        {
            "name": "Валера",
            "id_telegram": 155229,
            "media": "video",
            "path_dir": "D:\/test_media\/video",
            "id_message": 52266,
            "name_chanel": "name_chanel1",
            "link_chanel": "mychanel1",
            "id_telegram_chanel": "2345678765",
            "extension": "mp4"
        },
        {
            "name": "Jonh",
            "id_telegram": 155665929,
            "media": "audio",
            "path_dir": "D:\/test_media\/audio",
            "id_message": 65959,
            "name_chanel": "name_chanel2",
            "link_chanel": "mychanel2",
            "id_telegram_chanel": "23458765",
            "extension": "mp3"
        },
        {
            "name": "Tom KUKURUZE",
            "id_telegram": 15563359,
            "media": "image",
            "path_dir": "D:\/test_media\image",
            "id_message": 65959599,
            "name_chanel": "name_chanel3",
            "link_chanel": "mychanel3",
            "id_telegram_chanel": "234765",
            "extension": "jpeg"
        }
    ]
}

data_type_media = {
    "for": "add_data_in_bd",
    "data": [
        {
            "media": "video",
            "path_dir": "/path/video",
        }
    ]
}


def add_data_in_bd(list_data):
    for data in list_data["data"]:
        session = sessionmaker(bind=engine)
        s = session()

        author_one = Users(name=data["name"], id_telegram=data["id_telegram"])
        s.add(author_one)
        s.commit()

        id_user = author_one.id_user

        type_media = TypeMedia(type_media=data["media"], path_dir=data["path_dir"], extension=data['extension'])
        s.add(type_media)
        s.commit()

        id_type_media = type_media.id_type_media

        chanels = Chanels(name_chanel=data["name_chanel"], link_chanel=data["link_chanel"],
                          id_telegram=data["id_telegram_chanel"])
        s.add(chanels)
        s.commit()

        id_chanel = chanels.id_chanel

        media_contents = MediaContens(id_type_media=id_type_media, local_path=data["path_dir"], id_user=id_user)
        s.add(media_contents)
        s.commit()

        id_media = media_contents.id_media

        events = Events(id_message=data["id_message"], id_media=id_media, id_chanel=id_chanel, id_user=id_user)
        s.add(events)
        s.commit()
        s.close()


def add_types_media(data):
    session = sessionmaker(bind=engine)
    s = session()
    type_media = TypeMedia(type_media=data["media"], path_dir=data["path_dir"])
    s.add(type_media)
    s.commit()
    s.close()


def drop_tables():
    Events.__table__.drop(engine)
    MediaContens.__table__.drop(engine)
    TypeMedia.__table__.drop(engine)
    Users.__table__.drop(engine)
    Chanels.__table__.drop(engine)


drop_tables()
#add_data_in_bd(list_data)
