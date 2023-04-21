import datetime

from sqlalchemy.orm import relationship

from models.init_bd import Base
from models.media_tags_model import TagModel, tags
from models.mixins import ModelDbExt
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Text


class TypeMediaModel(Base, ModelDbExt):
    __tablename__ = "types_media"

    id_type_media = Column(Integer, primary_key=True)
    type_media = Column(String(20), nullable=False)
    name_dir = Column(String(250), nullable=False)
    extension = Column(String(20), nullable=False)


class MediaContentModel(Base, ModelDbExt):
    __tablename__ = "media_contents"

    id_media = Column(Integer, primary_key=True)
    id_type_media = Column(Integer, ForeignKey("types_media.id_type_media"), nullable=False)
    name_file = Column(String(250), nullable=False)
    description = Column(Text)
    date_download = Column(DateTime, nullable=False, default=datetime.datetime.now)
    last_time_used = Column(DateTime, nullable=False, onupdate=datetime.datetime.now,
                               default=datetime.datetime.now)
    id_user = Column(Integer, ForeignKey("users.id_user"), nullable=False)
    is_archive = Column(Boolean, nullable=False, default=False)
    type_media = relationship(TypeMediaModel, backref='types_media', uselist=False, lazy='subquery')
    tags = relationship(TagModel, secondary=tags, lazy='subquery')

    def __init__(self, id_user, id_type_media, name_file, description=None):
        self.id_type_media = id_type_media
        self.name_file = name_file
        self.id_user = id_user
        self.description = description
