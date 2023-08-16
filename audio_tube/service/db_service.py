from sqlalchemy.orm import Session
from models.users import User
from models.user_settings import UserSettings
from config import MIN_DIFF_DOWNLOAD
import datetime


def is_user_already_created(telegram_id: int, session: Session) -> bool:
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    return True if user is not None else False


def is_can_download_podcast(telegram_id: int, session: Session) -> bool:
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    if user.date_last_podcast_download is None:
        return True

    check_date = user.date_last_podcast_download + datetime.timedelta(
        minutes=MIN_DIFF_DOWNLOAD)
    return datetime.datetime.now() > check_date


# create
def create_user(telegram_id: int, session: Session) -> User:
    user = User(telegram_id=telegram_id)
    session.add(user)
    session.commit()
    return user


def create_user_settings(user_id: int, session: Session) -> UserSettings:
    settings = UserSettings()
    settings.user_id = user_id
    session.add(settings)
    session.commit()
    return settings


# get
def get_user_settings(telegram_id: int, session: Session) -> UserSettings:
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    return user.settings


def get_settings_caption(telegram_id: int, session: Session) -> int:
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    settings: UserSettings = user.settings
    return settings.caption_length


# update
def update_settings_caption(telegram_id: int, session: Session,
                            new_length: int) -> UserSettings:
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    settings: UserSettings = user.settings
    settings.caption_length = new_length
    session.add(settings)
    session.commit()
    return settings


def update_date_last_podcast_download(telegram_id: int, session: Session) -> User:
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    user.date_last_podcast_download = datetime.datetime.now()
    session.add(user)
    session.commit()
    return user


def update_count_of_downloaded_podcast(telegram_id: int, session: Session) -> User:
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    user.count_of_downloaded_podcasts += 1
    session.add(user)
    session.commit()
    return user


# admin panel

def get_all_users_count(session: Session) -> int:
    return len(session.query(User).all())


def get_count_of_active_users_per_days(session: Session, days: int) -> int:
    return len(session.query(User).filter(
        User.date_last_podcast_download > datetime.datetime.now() -
        datetime.timedelta(days=days)).all())
    

def get_total_count_of_downloaded_podcasts(session: Session) -> int:
    users = session.query(User).all()
    return sum(user.count_of_downloaded_podcasts for user in users)
