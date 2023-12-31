GREETINGS = """Привет!.

Это бот, который поможет тебе сделать из видео на YouTube полноценный подкаст для \
фонового прослушивания.

Используйте команду /help, чтобы получить справку по использованию бота.
"""

CMD_HELP_TEXT = """
Справка по использованию бота:
    /set_caption - установить новое значение для количества символом к описанию подкаста

Отправьте ссылку на видео и получите извлеченную аудио-дорожку для фонового прослушивания  
"""

SET_CAPTION_TEXT = """
Привет, пришли новую длину к описанию подкаста - от 0 до 150.
     0 - отсутствие текст
     150 - максимальная длина

Введенное значение не может превышать лимит (при превышении будет установлено значение \
150 символов).

Текущая длина - <b>{} символов</b>
"""
SET_CAPTION_TEXT_ERROR = """
Новое значение должно содержать только цифры.
Введение размер описание: от 0 до 150.

Текущая длина - <b>{} символов</b>
"""

SET_CAPTION_TEXT_SUCCESS = """
Новое значение описания к подкасту (<b>{} символов</b>) установлено!
"""

SET_IS_DELETE_LINK = """
Автоматическое удаление ссылки после отправки загруженного подкаста.

Хотите ли вы, чтобы оправленная ссылка после загрузки удалялась мной автоматически? \
(Да / Нет)
"""

DOWNLOAD_PODCAST_IS_NO_ABILITY = """
Загружать подкасты можно раз в 3 минуты.
"""

ADMIN_STATISTIC_TEXT = """
Информация по использованию бота:

Количество зарегистрированных пользователей:  <b>{}</b>
Количество активных пользователей за прошедшие сутки: <b>{}</b>
Количество активных пользователей за неделю: <b>{}</b>
Количество активных пользователей за месяц: <b>{}</b>

Общее количество загруженных подкастов: <b>{}</b>
"""
