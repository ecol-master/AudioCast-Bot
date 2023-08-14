from sqlalchemy.orm import Session
from models.users import User
from models.user_settings import UserSettings


def user_is_already_created(telegram_id: int, session: Session) -> bool:
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    return True if user is not None else False


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


def update_settings_caption(telegram_id: int, session: Session,
                            new_length: int) -> UserSettings:
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    settings: UserSettings = user.settings
    settings.caption_length = new_length
    session.add(settings)
    session.commit()
    return settings
