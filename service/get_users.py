import sys
from pathlib import Path

import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

path_proj = Path(__file__).resolve().parents[1]
sys.path.insert(1, str(path_proj))
from config import Config
from sheme_bd import Users

engine = create_engine(Config.SQLALCHEMY_DATABASE, echo=True)


@click.command()
def get_users():
    """Get list all user """
    session = sessionmaker(bind=engine)
    s = session()
    try:
        users = s.query(Users).all()
    except Exception as ex:
        click.echo(f"Error BD: {ex}")
        s.close()
        return
    for user in users:
        click.echo(user.serialize)
    s.close()


if __name__ == '__main__':
    get_users()
