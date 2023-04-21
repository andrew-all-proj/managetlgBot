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
    data = s.query(TypeMedia).all()
    for record in data:
        name_file = os.path.basename(record.path_dir)
        print(name_file)
        record.path_dir = name_file
    s.commit()




del_path()