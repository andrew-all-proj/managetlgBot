import sys
from datetime import datetime, timedelta

from sqlalchemy import func, literal_column, and_
from sqlalchemy.orm import sessionmaker
from pathlib import Path
path_proj = Path(__file__).resolve().parents[1]
sys.path.insert(1, str(path_proj))
from sheme_bd import engine, Users, MediaContens, Events, TypeMedia, Chanels, MediaTags, Tags

session = sessionmaker(bind=engine)
s = session()
time = datetime.now() + timedelta(hours=100)
records = s.query(Events, MediaContens, TypeMedia, func.string_agg(Tags.name, literal_column("', '")).label("tags")). \
            join(MediaContens, MediaContens.id_media == Events.id_media). \
            join(TypeMedia, TypeMedia.id_type_media == MediaContens.id_type_media). \
            join(MediaTags, MediaTags.id_media == MediaContens.id_media, isouter=True). \
            join(Tags, Tags.id_tag == MediaTags.id_tag, isouter=True). \
            group_by(Events, MediaContens, TypeMedia). \
            filter(and_(Events.id_chanel == 1, Events.completed == False,
                        Events.date_start < time)).order_by(Events.date_start).all()

for record in records:
    print(record)