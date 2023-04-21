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
@click.option('--id', prompt='id user', help='id user in telegram')
@click.option('-c', prompt='remove user? (yes - y, no - n)', default='n', help='(yes - y, no - n)')
def remove_user(id, c):
    """Remove user --rm <id telegram>"""
    if c.strip() == 'y':
        try:
            id = int(id)
        except:
            click.echo(f"Error id > digits")
            return
        session = sessionmaker(bind=engine)
        s = session()
        try:
            user = s.query(Users).filter(Users.id_telegram == id).one()
            s.delete(user)
            s.commit()
        except Exception as ex:
            s.rollback()
            click.echo(f"Error BD: {ex}")
            return
        click.echo(f"id: {id}")
        click.echo(f"removed successfully!")


if __name__ == '__main__':
    remove_user()
