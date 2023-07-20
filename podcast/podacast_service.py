import requests
from yt_dlp import YoutubeDL
from yt_dlp.utils import UnsupportedError, DownloadError
from utils import PodcastData, Preview
from .exceptions import CantDownloadVideoError
from pathlib import Path
from config import OUTPUT_DIR


def download(url: str) -> PodcastData:
    ydl_options = {
        # "logger": YTDlpLogger(),
        'writesubtitles': True,
        'skip-download': True,
        'outtmpl': f'./{OUTPUT_DIR}/%(title)s.%(ext)s'
    }
    try:
        with YoutubeDL(ydl_options) as ydl:
            info_dict: dict = ydl.extract_info(url, download=False)
            ydl.download([url])
            return _parse_video_data(ydl, info_dict)
    except DownloadError:
        raise CantDownloadVideoError
    except UnsupportedError:
        raise CantDownloadVideoError


def _parse_video_data(ydl: YoutubeDL, info: dict) -> PodcastData:
    preview_url = _parse_preview_url(info)
    filename = _parse_filename(ydl=ydl, info=info)
    preview_path = _download_preview(
        preview_url=preview_url,
        filename=filename
    )

    return PodcastData(
        filename=filename,
        url=info.get("webpage_url", None),
        title=info.get("title", None),
        author=info.get("uploader", None),
        duration=info.get("duration", None),
        preview_path=preview_path
    )


def _parse_preview_url(info: dict) -> str:
    thumbs = list(filter(lambda thumb: thumb["id"] == "41", info.get("thumbnails", [])))
    if not thumbs:
        raise CantDownloadVideoError
    return thumbs[0]["url"]


def _parse_filename(ydl: YoutubeDL, info: dict) -> str:
    name = ydl.prepare_filename(info)
    if name.startswith(f"{OUTPUT_DIR}\\"):
        name = name[5:]
    filename = f"{'.'.join(name.split('.')[:-1])}"
    return filename


def _download_preview(filename: str, preview_url: str) -> Preview:
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
    }
    response = requests.get(url=preview_url, headers=headers,
                            stream=True)
    if response.status_code != 200:
        preview_path = Path(f"{OUTPUT_DIR}", "default_thumb.jpg")
        # LOG print("Image couldn't be retrieved")
        return preview_path
    preview_path = Path(f"{OUTPUT_DIR}", f"{filename}.jpg")
    with open(f"{preview_path}", 'wb') as f:
        f.write(response.content)
        # LOG print('Image successfully downloaded: ', f"./img/{self.filename}.jpg")
        return preview_path
