import sqlalchemy
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec
import logging
from pathlib import Path
import os

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(db_file):
    global __factory
    
    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    check_exists_db_folder()

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    logging.info(f"Подключение к базе данных по адресу {conn_str}")

    engine = sqlalchemy.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)
    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()

def check_exists_db_folder() -> None:
    db_dir = Path("db")
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
