import sqlalchemy as sa
from .db_session import SqlAlchemyBase


class UserSettings(SqlAlchemyBase):
    __tablename__ = 'user_settings'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    caption_length = sa.Column(sa.Integer, default=50)
    is_del_link = sa.Column(sa.Boolean, default=True)
    min_diff_download = sa.Column(sa.Integer, default=3) # in minutes
