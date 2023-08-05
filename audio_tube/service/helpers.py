from aiogram import types


def get_message_urls(message: types.Message) -> list[str]:
    entities: list[types.MessageEntity] = message.entities
    if not entities:
        return []

    urls = [item.extract_from(message.text) for item in entities if item.type == "url"]
    return urls
