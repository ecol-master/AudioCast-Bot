from typing import Callable, Dict, Any, Awaitable
from fluentogram import TranslatorHub
from aiogram import BaseMiddleware, types
from service import db_service
from models import db_session


class TranslatorRunnerMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]],
            event: types.Message,
            data: Dict[str, Any]
    ) -> Any:
        hub: TranslatorHub = data.get('_translator_hub')
        session = db_session.create_session()
        try:
            language_code = db_service.get_user_lang(
                telegram_id=event.from_user.id, session=session
            )
        except AttributeError:
            language_code = "ru" if event.from_user.language_code == "ru" else "en"

        data['i18n'] = hub.get_translator_by_locale(language_code)
        return await handler(event, data)
