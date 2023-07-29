from yt_dlp import YoutubeDL
from dataclasses import dataclass
from pathlib import Path
from config import OUTPUT_DIR, PREVIEW_WIDTH, PREVIEW_HEIGHT
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


YDL_OPTIONS = {
    # "logger": YTDlpLogger(),
    'writesubtitles': True,
    'skip-download': True,
    'outtmpl': f'./{OUTPUT_DIR}/%(title)s.%(ext)s',
    "format": "139"
}


def _parse_podcast_data(filename: str, info: dict) -> Podcast:
    return Podcast(
        audio=types.FSInputFile(path=Path("data", f"{filename}.m4a")),
        caption=_parse_caption(info),
        title=info.get("title", ""),
        performer=info.get("uploader", ""),
        duration=info.get("duration", 0),
        thumb=types.FSInputFile(path=Path("data", f"{filename}.jpg"))
    )


def _parse_caption(info: dict) -> str:
    caption = info.get("description", "")
    if len(caption) > 150:
        return f"{caption[:150]}..."
    return caption


def _parse_preview_url(info: dict) -> str:
    thumbnails = info.get("thumbnails", [])
    if not thumbnails:
        raise CantDownloadAudioError
    preview_resolution = f"{PREVIEW_WIDTH}x{PREVIEW_HEIGHT}"
    thumb = [th for th in thumbnails if
             th.get("resolution", "") == preview_resolution]
    if not thumb:
        return info.get("thumbnail", "")
    else:
        return thumb[0]["url"]


def _parse_filename(ydl: YoutubeDL, info: dict) -> str:
    name = ydl.prepare_filename(info)
    if name.startswith(f"{OUTPUT_DIR}\\"):
        name = name[len(OUTPUT_DIR) + 1:]
    filename = f"{'.'.join(name.split('.')[:-1])}"
    return filename


class YTDlpLogger:
    def debug(self, msg):
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith("[youtube] "):
            self.info(msg)

    def info(self, msg):
        logging.info(msg)
