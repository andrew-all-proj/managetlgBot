import datetime
from sqlalchemy.orm import relationship

from models.init_bd import Base
from models.mixins import ModelDbExt
from sqlalchemy import Column, ForeignKey, Integer,  DateTime, Boolean

from models.posts_model import PostsModel



class EventModel(Base, ModelDbExt):
    __tablename__ = "events"

    id_event = Column(Integer, primary_key=True)
    id_post = Column(Integer, ForeignKey("posts.id_post"), nullable=False)
    id_message = Column(Integer)
    id_channel = Column(Integer, ForeignKey("channels.id_channel"), nullable=False)
    date_start = Column(DateTime, nullable=False, default=datetime.datetime.now)
    date_stop = Column(DateTime)
    completed = Column(Boolean, nullable=False, default=False)
    published = Column(Boolean, nullable=False, default=False)
    post = relationship(PostsModel, backref='posts', uselist=False, lazy='subquery')

    def __init__(self, id_post, id_channel, date_start, date_stop=None, id_message=None, completed=False,
                 published=False):
        self.id_post = id_post
        self.id_channel = id_channel
        self.date_start = date_start
        self.date_stop = date_stop
        self.id_message = id_message
        self.completed = completed
        self.published = published


class EventModelAll:
    items = None
    total_count = None