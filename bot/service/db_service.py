from sqlalchemy.orm import Session
from bot.models.users import User
from bot.models.user_settings import UserSettings
import bot.config as config
import datetime

bot_config = config.get_bot_config()

def is_user_already_created(telegram_id: int, session: Session) -> bool:
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    return True if user is not None else False


def is_can_download_podcast(telegram_id: int, session: Session) -> bool:
    if telegram_id == bot_config.admin_id:
        return True

    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    if user.date_last_podcast_download is None:
        return True
    settings: UserSettings = user.settings
    check_date = user.date_last_podcast_download + datetime.timedelta(
        minutes=settings.min_diff_download)
    return datetime.datetime.now() > check_date


# create
def create_user(telegram_id: int, session: Session, lang: str) -> User:
    user = User(telegram_id=telegram_id, lang=lang)
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


def get_user_lang(telegram_id: int, session: Session) -> str:
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    return user.lang

# update
def update_date_last_podcast_download(telegram_id: int, session: Session) -> User:
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    user.date_last_podcast_download = datetime.datetime.now()
    session.add(user)
    session.commit()
    return user

def update_lang(telegram_id: int, session: Session, new_lang: str) -> User:
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    user.lang = new_lang
    session.add(user)
    session.commit()
    return user

def update_count_of_downloaded_podcast(telegram_id: int, session: Session) -> User:
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    user.count_of_downloaded_podcasts += 1
    session.add(user)
    session.commit()
    return user

def update_settings_caption(telegram_id: int, session: Session,
                            new_length: int) -> UserSettings:
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    settings: UserSettings = user.settings
    settings.caption_length = new_length
    session.add(settings)
    session.commit()
    return settings

def update_setting_is_del_link(telegram_id: int, session: Session, is_del_link: bool) -> UserSettings:
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    settings: UserSettings = user.settings
    settings.is_del_link = is_del_link
    session.add(settings)
    session.commit()
    return settings

def update_min_diff_download(telegram_id: int, session: Session, new_value: int) -> UserSettings:
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    settings: UserSettings = user.settings
    settings.min_diff_download = new_value
    session.add(settings)
    session.commit()
    return settings


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
