import asyncio
from yt_dlp import YoutubeDL
from yt_dlp.utils import UnsupportedError, DownloadError
from service import Podcast, YDL_OPTIONS, CantDownloadAudioError, DurationLimitError
from pathlib import Path
import requests
from config import OUTPUT_DIR, PREVIEW_WIDTH, PREVIEW_HEIGHT, MAX_PODCAST_DURATION
from aiogram import types


class PodcastMaker:
    def __init__(self, url: str):
        self.url = url
        self.ydl = YoutubeDL(YDL_OPTIONS)
        self.podcast_info = self.ydl.extract_info(url, download=False)
        self.filename = self._parse_filename()

    def get_podcast_data(self) -> Podcast:
        duration = self.podcast_info.get("duration", 0)
        if duration > MAX_PODCAST_DURATION:
            raise DurationLimitError
        return Podcast(
            audio=types.FSInputFile(path=Path("data", f"{self.filename}.m4a")),
            caption=self._parse_caption(),
            title=self.podcast_info.get("title", ""),
            performer=self.podcast_info.get("uploader", ""),
            duration=duration,
            thumb=types.FSInputFile(path=Path("data", f"{self.filename}.jpg"))
        )

    async def download(self):
        tasks = [
            asyncio.create_task(self.download_audio()),
            asyncio.create_task(self.download_preview())
        ]
        await asyncio.gather(*tasks)

    async def download_audio(self):
        try:
            self.ydl.download(self.url)
        except DownloadError:
            raise CantDownloadAudioError
        except UnsupportedError:
            raise CantDownloadAudioError

    async def download_preview(self):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
        }
        preview_url = self._parse_preview_url()
        response = requests.get(url=preview_url, headers=headers, stream=True)
        if response.status_code == 200:
            preview_path = Path(f"{OUTPUT_DIR}", f"{self.filename}.jpg")
            with open(f"{preview_path}", 'wb') as f:
                f.write(response.content)

    def _parse_caption(self) -> str:
        caption = self.podcast_info.get("description", "")
        if len(caption) > 150:
            return f"{caption[:150]}..."
        return caption

    def _parse_preview_url(self) -> str:
        thumbnails = self.podcast_info.get("thumbnails", [])
        if not thumbnails:
            raise CantDownloadAudioError
        preview_resolution = f"{PREVIEW_WIDTH}x{PREVIEW_HEIGHT}"
        thumb = [th for th in thumbnails if
                 th.get("resolution", "") == preview_resolution]
        if not thumb:
            return self.podcast_info.get("thumbnail", "")
        else:
            return thumb[0]["url"]

    def _parse_filename(self) -> str:
        name = self.ydl.prepare_filename(self.podcast_info)
        if name.startswith(f"{OUTPUT_DIR}\\"):
            name = name[len(OUTPUT_DIR) + 1:]
        filename = f"{'.'.join(name.split('.')[:-1])}"
        return filename
