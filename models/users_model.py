import datetime
from sqlalchemy.orm import relationship


from models.auth_model import AuthHistoryModel
from models.channels_model import UserChannelModel, ChannelModel
from models.init_bd import Base
from models.media_contents_model import MediaContentModel
from models.mixins import ModelDbExt
from sqlalchemy import Column,  Integer, String, DateTime, Boolean

from models.posts_model import PostsModel


class UserModel(Base, ModelDbExt):
    __tablename__ = "users"

    id_user = Column(Integer, primary_key=True)
    user_name = Column(String(30), nullable=False)
    id_telegram = Column(String(50), unique=True)
    email = Column(String(50), unique=True, nullable=False, default=False)
    confirmed = Column(Boolean, nullable=False, default=False)
    password = Column(String(128), nullable=False)
    date_registration = Column(DateTime, nullable=False, default=datetime.datetime.now)
    data_update = Column(DateTime, nullable=False, onupdate=datetime.datetime.now, default=datetime.datetime.now)
    role = Column(String(30), nullable=False, default="user")
    is_archive = Column(Boolean, nullable=False, default=False)
    media = relationship(MediaContentModel)
    posts = relationship(PostsModel)
    user_channel = relationship(UserChannelModel)
    admin_channel = relationship(ChannelModel)
    auth = relationship(AuthHistoryModel)

    def __init__(self, email, password, user_name, id_telegram=None, is_archive=False):
        self.user_name = user_name
        self.id_telegram = id_telegram
        self.email = email
        self.is_archive = is_archive
        self.hash_password(password)

    def confirmed_email(self, res):
        self.confirmed = res
