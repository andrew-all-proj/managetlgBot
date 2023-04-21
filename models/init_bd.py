from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import Config


Base = declarative_base()
engine = create_engine(Config.SQLALCHEMY_DATABASE)  # , echo=True
session = sessionmaker(bind=engine)
s = session()
