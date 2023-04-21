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
@click.option('--name', prompt='User name', help='Name super user')
@click.option('--id', prompt='id user', help='id user in telegram')
@click.option('-c', prompt='Create super user? (yes - y, no - n)', default='n', help='(yes - y, no - n)')
def create_super_user(name, id, c):
    """Create super user (--user <str>) Your telegramn id (--id <int>)"""
    if c.strip() == 'y':
        try:
            id = int(id)
        except:
            click.echo(f"Error id > digits")
            return
        try:
            session = sessionmaker(bind=engine)
            s = session()
            author_one = Users(name=name.strip(), id_telegram=id, role=True)
            s.add(author_one)
            s.commit()
            s.close()
        except Exception as ex:
            s.rollback()
            click.echo(f"Error BD: {ex}")
            s.close()
            return
        click.echo(f"name: {name}")
        click.echo(f"id: {id}")
        click.echo(f"created successfully!")


if __name__ == '__main__':
    create_super_user()
