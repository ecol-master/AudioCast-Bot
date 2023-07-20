from pathlib import Path
import moviepy.editor
from utils import Podcast, PodcastData
from aiogram import types
from .podacast_service import download
from .exceptions import CantCutAudio
from config import OUTPUT_DIR


def cut_audio(video_data: PodcastData) -> Path:
    try:
        video_path = Path(f"{OUTPUT_DIR}", f"{video_data.filename}.mp4")
        video = moviepy.editor.VideoFileClip(f"{video_path}")
        audio = video.audio
        audio_path = Path(f"{OUTPUT_DIR}", f"{video_data.filename}.mp3")
        audio.write_audiofile(audio_path)
        return audio_path
    except Exception as _err:
        print("MOVIEPY ERROR", _err)
        raise CantCutAudio


def make_podcast(url: str) -> Podcast:
    video_data = download(url=url)
    audio_path = cut_audio(video_data)
    return Podcast(
        audio=types.FSInputFile(path=audio_path),
        caption="Описание видео",
        title=video_data.title,
        performer=video_data.author,
        duration=video_data.duration,
        thumb=types.FSInputFile(path=f"{video_data.preview_path}")
    )
