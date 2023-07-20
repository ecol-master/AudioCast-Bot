from typing import NamedTuple
from enum import Enum
from aiogram import types
from pathlib import Path

Preview = Path


class ResultStatus(Enum):
    OK = "ok"
    ERROR = "error"


class PodcastData(NamedTuple):
    filename: str
    url: str
    title: str
    author: str
    duration: int
    preview_path: Preview


class Podcast(NamedTuple):
    audio: types.FSInputFile
    caption: str
    title: str
    performer: str
    duration: int
    thumb: types.FSInputFile
