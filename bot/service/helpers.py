from aiogram import types
from bot.config import OUTPUT_DIR
from pathlib import Path
import asyncio
import os
import logging
from fluentogram import TranslatorHub, FluentTranslator
from fluent_compiler.bundle import FluentBundle


def get_message_urls(message: types.Message) -> list[str]:
    entities: list[types.MessageEntity] | None = message.entities
    if not entities:
        return []

    urls = [item.extract_from(message.text) for item in entities if item.type == "url" and message.text]
    return urls


# async remove downloaded files
async def rm_downloaded_files(filename: str):
    content = os.listdir(Path(f"{OUTPUT_DIR}"))
    downloaded_files = filter(lambda f: f.startswith(filename), content)

    async with asyncio.TaskGroup() as tg:
        for file in downloaded_files:
            tg.create_task(remove_file(file))

async def remove_file(file: str):
    os.remove(Path(f"{OUTPUT_DIR}", file))
    logging.info(f"Delete file: {file}")



def validate_new_caption_length(new_length: str) -> int:
    if not new_length.isdecimal() or not new_length:
        raise ValueError
    new_length = int(new_length)
    return 150 if new_length > 150 else new_length


def validate_answer_del_link(ans: str) -> bool:
    if ans.strip().lower() in ("да", "yes"):
        return True
    if ans.strip().lower() in ("нет", "no"):
        return False
    raise ValueError

def get_translator_hub() -> TranslatorHub:
    ru_filenames = [
        "./bot/locales/ru/menu_ru.ftl", "./bot/locales/ru/base_cmd_ru.ftl", "./bot/locales/ru/buttons_ru.ftl",
        "./bot/locales/ru/admin_ru.ftl"  
    ]
    en_filenames = [
        "./bot/locales/en/menu_en.ftl", "./bot/locales/en/base_cmd_en.ftl", "./bot/locales/en/buttons_en.ftl",
        "./bot/locales/en/admin_en.ftl"
    ]

    return TranslatorHub(
        locales_map={
            "en": ("en", ),
            "ru":("ru", "en",)
        },
        translators=[
            FluentTranslator(
                locale="ru",
                translator=FluentBundle.from_files("ru", filenames=ru_filenames)
            ),
            FluentTranslator(
                locale="en",
                translator=FluentBundle.from_files("en-US", filenames=en_filenames)
            )
        ]
    )
