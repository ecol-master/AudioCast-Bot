import datetime
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    telegram_id = sa.Column(sa.Integer)
    date_start_bot = sa.Column(sa.DateTime, default=datetime.datetime.now)
    settings = relationship("UserSettings", uselist=False, backref="users")
