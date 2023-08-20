from dataclasses import dataclass
from config import OUTPUT_DIR
import logging
from aiogram import types


@dataclass
class Podcast:
    filename: str
    audio: types.FSInputFile
    caption: str
    title: str
    performer: str
    duration: str
    thumbnail: types.FSInputFile

    def as_dict(self):
        values = self.__dict__
        return {k: values[k] for k in values.keys() if k != "filename"}


class CantDownloadAudioError(Exception):
    """Program can't download video."""


class DurationLimitError(Exception):
    """Too long podcast for download."""


class YDLLogger:
    def debug(self, msg):
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if not msg.startswith("[download] "):
            logging.debug(msg)

    def info(cls, msg):
        logging.info(msg)

    def warning(cls, msg):
        logging.warning(msg)

    def error(cls, msg):
        logging.error(msg)


YDL_OPTIONS = {
    "logger": YDLLogger(),
    'writesubtitles': False,
    'skip-download': False,
    'outtmpl': f'./{OUTPUT_DIR}/%(title)s.%(ext)s',
    "format": "139"
}
