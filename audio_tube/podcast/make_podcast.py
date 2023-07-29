import requests
from yt_dlp import YoutubeDL
from yt_dlp.utils import UnsupportedError, DownloadError
from .podacast_service import Podcast, YDL_OPTIONS, _parse_filename, _parse_preview_url, \
    _parse_podcast_data, CantDownloadAudioError
from pathlib import Path
from config import OUTPUT_DIR
import logging


def make_podcast(url: str) -> Podcast:
    try:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info_dict: dict = ydl.extract_info(url, download=False)
            filename = _parse_filename(ydl=ydl, info=info_dict)
            preview_url = _parse_preview_url(info=info_dict)
            _download_preview(filename=filename, preview_url=preview_url)
            ydl.download([url])
            return _parse_podcast_data(filename=filename, info=info_dict)
    except DownloadError:
        raise CantDownloadAudioError
    except UnsupportedError:
        raise CantDownloadAudioError;


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
