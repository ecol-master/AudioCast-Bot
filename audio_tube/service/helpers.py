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



def validate_new_caption_length(new_length: str) -> int:
    if not new_length.isdecimal() or not new_length:
        raise ValueError
    new_length = int(new_length)
    return 150 if new_length > 150 else new_length

def validate_answer_del_link(ans: str) -> bool:
    if ans.strip().lower() == "да":
        return True
    if ans.strip().lower() == "нет":
        return False
    raise ValueError