from yt_dlp import YoutubeDL
from yt_dlp.utils import UnsupportedError, DownloadError
from service import Podcast, YDL_OPTIONS, CantDownloadAudioError
from pathlib import Path
import requests
from config import OUTPUT_DIR, PREVIEW_WIDTH, PREVIEW_HEIGHT
from aiogram import types
import json


def make_podcast(url: str) -> tuple[Podcast, str]:
    try:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info_dict: dict = ydl.extract_info(url, download=False)
            filename = _parse_filename(ydl=ydl, info=info_dict)
            preview_url = _parse_preview_url(info=info_dict)
            _download_preview(filename=filename, preview_url=preview_url)
            ydl.download([url])
            return _parse_podcast_data(filename=filename, info=info_dict), filename
    except DownloadError:
        raise CantDownloadAudioError
    except UnsupportedError:
        raise CantDownloadAudioError


def _download_preview(filename: str, preview_url: str):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
    }
    response = requests.get(url=preview_url, headers=headers, stream=True)
    if response.status_code != 200:
        preview_path = Path(f"{OUTPUT_DIR}", "default_thumb.jpg")
        # LOG print("Image couldn't be retrieved")
        return preview_path
    preview_path = Path(f"{OUTPUT_DIR}", f"{filename}.jpg")
    with open(f"{preview_path}", 'wb') as f:
        f.write(response.content)
        # LOG print('Image successfully downloaded: ', f"./img/{self.filename}.jpg")
        return preview_path


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
