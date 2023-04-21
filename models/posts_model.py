import datetime
from sqlalchemy.orm import relationship

from models.init_bd import Base
from models.media_contents_model import MediaContentModel
from models.mixins import ModelDbExt
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean,  Table

media = Table('posts_media',
             Base.metadata,
             Column('id_post', Integer, ForeignKey('posts.id_post'), primary_key=True),
             Column('id_media', Integer, ForeignKey('media_contents.id_media'), primary_key=True)
             )


class PostsModel(Base, ModelDbExt):
    __tablename__ = "posts"

    id_post = Column(Integer, primary_key=True)
    text = Column(String(3000))
    id_user = Column(Integer, ForeignKey("users.id_user"), nullable=False)
    date_create = Column(DateTime, nullable=False, default=datetime.datetime.now)
    data_update = Column(DateTime, nullable=False, onupdate=datetime.datetime.now, default=datetime.datetime.now)
    is_archive = Column(Boolean, nullable=False, default=False)
    media = relationship(MediaContentModel, secondary=media, lazy='subquery')

    def __init__(self, id_user, text=None):
        self.text = text
        self.id_user = id_user


class PostsModelAll:
    items = None
    total_count = None
