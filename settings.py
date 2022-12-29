import telebot

TOKEN = "5486699586:AAFOL-pqTSn5cctJi95j8A8gHA0YW-6ed8M"
DB_CONFIG = dict(
    provider='postgres',
    user='postgres',
    password='jskoo1997',
    host='localhost',
    database='bot_db')
HELP_INFO = """   
/start - Начать работу.
/help - Вывести список доступных команд.
/add - Добавить задачу.
/show - Показать добавленные задачи.
/game - Поиграем?
/draw - Создать мем
/random - Добавление случайной задачи на Сегодня
/anime - Для избранных
/exit - Выход."""
RANDOM_THINGS = ["Прибухнуть", "Полежать", "Поесть"]
BOT_MENU_CONFIG = [
    telebot.types.BotCommand("/start", "Основное меню"),
    telebot.types.BotCommand("/help", "Вывести список доступных команд"),
    telebot.types.BotCommand("/add", "Добавить задачу"),
    telebot.types.BotCommand("/show", "Показать добавленные задачи"),
    telebot.types.BotCommand("/game", "Поиграем?"),
    telebot.types.BotCommand("/draw", "Создать мем"),
    telebot.types.BotCommand("/random", "Добавление случайной задачи на Сегодня"),
    telebot.types.BotCommand("/anime", "Для избранных"),
    telebot.types.BotCommand("/exit", "Выход"),
]