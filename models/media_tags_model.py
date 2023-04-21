

from models.init_bd import Base
from models.mixins import ModelDbExt
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint, Table

tags = Table('media_tags',
             Base.metadata,
             Column('id_tag', Integer, ForeignKey('tags.id_tag'), primary_key=True),
             Column('id_media', Integer, ForeignKey('media_contents.id_media'), primary_key=True)
             )


class TagModel(Base, ModelDbExt):
    __tablename__ = "tags"

    id_tag = Column(Integer, primary_key=True)
    tag_name = Column(String(50), nullable=False)
    id_channel = Column(Integer, ForeignKey("channels.id_channel"))
    __table_args__ = (UniqueConstraint('tag_name', 'id_channel', name='_tag_channel_uc'),)

    def __init__(self, tag_name, id_channel):
        self.tag_name = tag_name
        self.id_channel = id_channel
