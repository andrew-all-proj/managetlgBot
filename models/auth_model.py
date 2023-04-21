import datetime

from models.init_bd import Base
from models.mixins import ModelDbExt
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime


class AuthHistoryModel(Base, ModelDbExt):
    __tablename__ = "auth_history"

    id_auth_history = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey("users.id_user"), nullable=False)
    date_auth = Column(DateTime, nullable=False, default=datetime.datetime.now)
    from_is = Column(String(300), nullable=False)

    def __init__(self, id_user, from_is):
        self.id_user = id_user
        self.from_is = from_is
