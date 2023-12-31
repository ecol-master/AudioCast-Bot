import datetime
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    telegram_id = sa.Column(sa.Integer)
    date_start_bot = sa.Column(sa.DateTime, default=datetime.datetime.now)
    date_last_podcast_download = sa.Column(sa.DateTime)
    count_of_downloaded_podcasts = sa.Column(sa.Integer, default=0)
    lang = sa.Column(sa.String, default="ru")

    settings = relationship("UserSettings", uselist=False, backref="users")
