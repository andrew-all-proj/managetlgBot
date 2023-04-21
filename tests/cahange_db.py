"""Удаления пути к файлу. Оставить только имя файла"""
import os
import sys

from sqlalchemy.orm import sessionmaker
from pathlib import Path
path_proj = Path(__file__).resolve().parents[1]
sys.path.insert(1, str(path_proj))
from sheme_bd import engine, Users, MediaContens, Events, TypeMedia, Chanels


def del_path():
    session = sessionmaker(bind=engine)
    s = session()
    data = s.query(MediaContens).all()
    for record in data:
        name_file = os.path.basename(record.local_path)
        print(name_file)
        record.local_path = name_file
    s.commit()




del_path()