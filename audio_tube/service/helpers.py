from aiogram import types
from config import OUTPUT_DIR
from pathlib import Path
import asyncio
import os
import logging


def get_message_urls(message: types.Message) -> list[str]:
    entities: list[types.MessageEntity] = message.entities
    if not entities:
        return []

    urls = [item.extract_from(message.text) for item in entities if item.type == "url"]
    return urls


# async remove downloaded files
async def rm_downloaded_files(filename: str):
    content = os.listdir(Path(f"{OUTPUT_DIR}"))
    downloaded_files = filter(lambda f: f.startswith(filename), content)
    tasks = []
    for file in downloaded_files:
        task = asyncio.create_task(remove_file(file))
        tasks.append(task)
    await asyncio.gather(*tasks)


async def remove_file(file: str):
    os.remove(Path(f"{OUTPUT_DIR}", file))
    logging.info(f"Delete file: {file}")
