from yt_dlp import YoutubeDL
from yt_dlp.utils import UnsupportedError, DownloadError
from audio_cast.service import Podcast, CantDownloadAudioError, DurationLimitError, YDL_OPTIONS, \
    Url
from audio_cast.config import OUTPUT_DIR, PREVIEW_WIDTH, PREVIEW_HEIGHT, MAX_PODCAST_DURATION
from audio_cast.models.user_settings import UserSettings
from aiogram import types
from pathlib import Path
import requests
import json

ydl = YoutubeDL(YDL_OPTIONS)


def get_podcast(url: Url, settings: UserSettings) -> Podcast:
    info = ydl.extract_info(url, download=False)
    with open("info.json", "w") as file:
        json.dump(info, file)
    _validate_podcast_data(info)

    preview_url = _parse_preview_url(info=info)
    filename = _parse_filename(info=info)

    download(url=url, preview_url=preview_url, filename=filename)
    #_download_preview(filename, preview_url)
    return _parse_podcast_data(settings=settings, filename=filename, info=info)


def _validate_podcast_data(info: dict) -> None:
    duration = info.get("duration", 0)
    if duration > MAX_PODCAST_DURATION:
        raise DurationLimitError


def _parse_podcast_data(settings: UserSettings, filename: str, info: dict) -> Podcast:
    return Podcast(
        filename=filename,
        audio=types.FSInputFile(path=Path(f"{filename}.m4a")),
        caption=_validate_caption(caption=info.get("description", ""),
                                  caption_length=settings.caption_length),
        title=info.get("title", ""),
        performer=info.get("uploader", ""),
        duration=info.get("duration", 0),
        #thumbnail=types.FSInputFile(path=Path(f"{filename}.jpg")),
    )


def download(url: str, preview_url: str, filename: str) -> None:
    try:
        ydl.download(url)
        #_download_preview(filename=filename, preview_url=preview_url)
    except DownloadError:
        raise CantDownloadAudioError
    except UnsupportedError:
        raise CantDownloadAudioError


def _download_preview(filename: str, preview_url: str) -> None:
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
    }
    response = requests.get(url=preview_url, headers=headers, stream=True)
    if response.status_code == 200:
        preview_path = Path(f"{OUTPUT_DIR}", f"{filename}.jpg")
        with open(f"{preview_path}", 'wb') as f:
            f.write(response.content)


def _validate_caption(caption: str, caption_length: int) -> str:
    if not caption_length:
        return ""
    if len(caption) > caption_length:
        return f"{caption[:caption_length]}..."
    return caption


def _parse_preview_url(info: dict) -> Url:
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


def _parse_filename(info: str) -> str:
    name = ydl.prepare_filename(info)
    if name.startswith(f"{OUTPUT_DIR}\\"):
        name = name[len(OUTPUT_DIR) + 1:]
    filename = f"{'.'.join(name.split('.')[:-1])}"
    return filename
