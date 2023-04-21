"""Заполнение таблицы tags данными из файла tags.json"""

import json
import sys
from pathlib import Path

from sqlalchemy.orm import sessionmaker

path_proj = Path(__file__).resolve().parents[1]
sys.path.insert(1, str(path_proj))
from sheme_bd import engine, TypeMedia, Tags
from config import Config
path_proj = Path(__file__).parent


def add_types_media():
    with open(f"{path_proj}/list_tags.json", "r", encoding="UTF-8") as f:
        data = json.load(f)
        records = data["records"]

    session = sessionmaker(bind=engine)
    s = session()
    for record in records:
        try:
            tags = Tags(name=record["name"])
            s.add(tags)
            s.commit()
        except Exception as ex:
            s.rollback()
            print(f"ERROR: {ex}")
    s.close()
    print('OK')


if __name__ == '__main__':
    add_types_media()
