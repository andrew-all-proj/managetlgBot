"""Заполнение таблицы type_media данными из файла types_media.json"""

import json
import sys
from pathlib import Path

from sqlalchemy.orm import sessionmaker

path_proj = Path(__file__).resolve().parents[1]
sys.path.insert(1, str(path_proj))
from sheme_bd import engine, TypeMedia
from config import Config
path_proj = Path(__file__).parent


def add_types_media():
    with open(f"{path_proj}/types_media.json", "r", encoding="UTF-8") as f:
        data = json.load(f)
        records = data["records"]

    session = sessionmaker(bind=engine)
    s = session()
    for record in records:
        try:
            type_media = TypeMedia(type_media=record["media"], path_dir=f"{record['path_dir']}",
                                   extension=record['extension'])
            s.add(type_media)
            s.commit()
        except Exception as ex:
            s.rollback()
            print(f"ERROR: {ex}")
    s.close()


if __name__ == '__main__':
    add_types_media()
