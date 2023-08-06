from dataclasses import dataclass
from config import OUTPUT_DIR
import logging
from aiogram import types


@dataclass
class Podcast:
    audio: types.FSInputFile
    caption: str
    title: str
    performer: str
    duration: str
    thumb: types.FSInputFile


class CantDownloadAudioError(Exception):
    """Program can't download video."""


class DurationLimitError(Exception):
    """Too long podcast for download."""


class YDLLogger:
    def debug(self, msg):
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith("[youtube] "):
            self.info(msg)

    def info(self, msg):
        logging.info(msg)


YDL_OPTIONS = {
    # "logger": YTDlpLogger(),
    'writesubtitles': True,
    'skip-download': True,
    'outtmpl': f'./{OUTPUT_DIR}/%(title)s.%(ext)s',
    "format": "139"
}
