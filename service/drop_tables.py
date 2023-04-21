"""Удаление всех таблиц"""
import sys

from pathlib import Path
path_proj = Path(__file__).resolve().parents[1]
sys.path.insert(1, str(path_proj))
from sheme_bd import engine, Users, MediaContens, Events, TypeMedia, Chanels, Tags, MediaTags


def drop_tables():
    Events.__table__.drop(engine)
    MediaContens.__table__.drop(engine)
    TypeMedia.__table__.drop(engine)
    Users.__table__.drop(engine)
    Chanels.__table__.drop(engine)
    Tags.__table__.drop(engine)
    MediaTags.__table__.drop(engine)
    print("Удалено")

if __name__ == '__main__':
    drop_tables()