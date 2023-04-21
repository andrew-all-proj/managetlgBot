import datetime

from sqlalchemy.orm import relationship

from models.events_model import EventModel
from models.init_bd import Base
from models.media_tags_model import TagModel
from models.mixins import ModelDbExt
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean,  UniqueConstraint


class UserChannelModel(Base, ModelDbExt):
    __tablename__ = "users_channels"

    id_user_channel = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey("users.id_user"), nullable=False)
    id_channel = Column(Integer, ForeignKey("channels.id_channel"), nullable=False)
    __table_args__ = (UniqueConstraint('id_user', 'id_channel', name='_user_channel_uc'),)

    def __init__(self, id_channel, id_user):
        self.id_channel = id_channel
        self.id_user = id_user


class ChannelModel(Base, ModelDbExt):
    __tablename__ = "channels"

    id_channel = Column(Integer, primary_key=True)
    name_channel = Column(String(200), nullable=False)
    link_channel = Column(String(200), nullable=False)
    id_telegram = Column(String(200), nullable=False, unique=True)
    date_create = Column(DateTime, nullable=False, default=datetime.datetime.now)
    data_update = Column(DateTime, nullable=False, onupdate=datetime.datetime.now, default=datetime.datetime.now)
    is_archive = Column(Boolean, nullable=False, default=False)
    id_user_admin = Column(Integer, ForeignKey("users.id_user"), nullable=False)
    users_channels = relationship(UserChannelModel)
    tags = relationship(TagModel)
    event = relationship(EventModel)

    def __init__(self, id_user_admin, name_channel, link_channel, id_telegram):
        self.name_channel = name_channel
        self.link_channel = link_channel
        self.id_telegram = id_telegram
        self.id_user_admin = id_user_admin
