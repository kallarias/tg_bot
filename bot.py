import random
import telebot
import time
import logging
from telebot import types

from draw.draw_mem import PostCardMaker
from mastermind_engine import zagadka_chislo, proverka_chisla, _my_number

try:
    import settings
except ImportError:
    exit('DO settings.py.default settings.py and set TOKEN')

log = logging.getLogger("bot")


def configure_logging():
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    stream_handler.setLevel(logging.INFO)
    log.addHandler(stream_handler)

    file_handler = logging.FileHandler("bot.log", encoding='utf-8')
    file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    file_handler.setLevel(logging.DEBUG)
    log.addHandler(file_handler)
    log.setLevel(logging.DEBUG)


bot = telebot.TeleBot(settings.TOKEN)


help1 = """   
/start - Начать работу.
/help - Вывести список доступных команд.
/add - Добавить задачу.
/show - Показать добавленные задачи.
/game - Поиграем?
/draw - Создать мем
/random - Добавление случайной задачи на Сегодня
/exit - Выход."""
bd = {}
user_dict = {}
random_task = ["Прибухнуть", "Полежать", "Поесть"]
tconv = lambda x: time.strftime("%H:%M:%S %d.%m.%Y", time.localtime(x))  # Конвертация даты в читабельный вид
configure_logging()
bot.set_my_commands([
    telebot.types.BotCommand("/start", "Основное меню"),
    telebot.types.BotCommand("/help", "Вывести список доступных команд"),
    telebot.types.BotCommand("/add", "Добавить задачу"),
    telebot.types.BotCommand("/show", "Показать добавленные задачи"),
    telebot.types.BotCommand("/game", "Поиграем?"),
    telebot.types.BotCommand("/draw", "Создать мем"),
    telebot.types.BotCommand("/random", "Добавление случайной задачи на Сегодня"),
    telebot.types.BotCommand("/exit", "Выход"),
])


def add_bd(data, task):
    if data in bd:
        bd[data].append(task)
    else:
        bd[data] = [task]


class add_tasks:
    def __init__(tasks, name):
        tasks.name = name
        tasks.data = None
        tasks.task = None


@bot.message_handler(commands=['start'])
def send_welcome(message):
    log.debug(f"пришла команда start от {message.from_user.id}")
    log.info(f"пришла команда start от {message.from_user.id}")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    b_help = types.KeyboardButton('🙏🏻 Информация 🙏🏻')
    b_add = types.KeyboardButton('✏️ Добавить задачу ✏️')
    b_show = types.KeyboardButton('📝 Посмотреть задачи 📝')
    b_random = types.KeyboardButton('👁‍🗨 Магическая задача 👁‍🗨')
    b_exit = types.KeyboardButton('🫡 Попрощаться 🫡')
    b_game = types.KeyboardButton('🎮 Поиграем? 🎮')
    b_draw = types.KeyboardButton('🖼 Творим 🖼')
    markup.add(b_add, b_show, b_random, b_game, b_draw, b_exit, b_help)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}', reply_markup=markup)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, help1)


@bot.message_handler(commands=['add'])
def add(message):
    chat_id = message.chat.id
    name = message.from_user.first_name
    user = add_tasks(name)
    user_dict[chat_id] = user
    msg = bot.reply_to(message, "Введите дату:")
    bot.register_next_step_handler(msg, process_age_step)


def process_age_step(message):
    try:
        chat_id = message.chat.id
        data = message.text
        add_tasks = user_dict[chat_id]
        add_tasks.data = data
        msg = bot.reply_to(message, 'Введите задачу: ')
        bot.register_next_step_handler(msg, process_sex_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_sex_step(message):
    try:
        chat_id = message.chat.id
        task = message.text
        add_tasks = user_dict[chat_id]
        add_tasks.task = task
        add_bd(add_tasks.data, add_tasks.task)
        bot.send_message(chat_id, 'Добрый день ' + add_tasks.name + '\nЗадача ' + str(
            add_tasks.task) + ' записана на ' + add_tasks.data)
    except Exception as e:
        bot.reply_to(message, 'oooops')


@bot.message_handler(commands=['show'])
def show(message):
    msg = bot.reply_to(message, "Выберите дату:")
    bot.register_next_step_handler(msg, process_name_step1)


def process_name_step1(message):
    try:
        chat_id = message.chat.id
        data = message.text
        text = ""
        if data in bd:
            text = data.upper()
            for task in bd[data]:
                text = f'{text}\n❗️ {task} '
        else:
            text = data.upper()
            text = text + "\nДанных нет!"
        bot.send_message(chat_id, text)
    except Exception as e:
        bot.reply_to(message, 'oooops')


@bot.message_handler(commands=['random'])
def random_add(message):
    task = random.choice(random_task)
    data1 = tconv(message.date)
    command = data1.split()
    data = command[1]
    add_bd(data, task)
    bot.send_message(message.chat.id,
                     'Добрый день ' + message.from_user.first_name + '\nЗадача ' + task + ' записана на ' + data)


@bot.message_handler(commands=['game'])
def game(message):
    zagadka_chislo()
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        b_yes = types.KeyboardButton('✅ Да ✅')
        b_no = types.KeyboardButton('👽 Я пельмешек 👽')
        markup.add(b_yes, b_no)
        msg = bot.reply_to(message, '''Правила:\n
Компьютер задумывает четыре различные цифры из 0,1,2,...9.\n
Игрок делает ходы, чтобы узнать эти цифры и их порядок.\n
Каждый ход состоит из четырёх цифр, 0 может стоять на первом месте.\n
В ответ компьютер показывает число отгаданных цифр,
стоящих на своих местах (число быков) и число отгаданных 
цифр, стоящих не на своих местах (число коров). \n\nНачинаем?''', reply_markup=markup)
        bot.register_next_step_handler(msg, process_game)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_game(message):
    if message.text == '✅ Да ✅':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        b_lox = types.KeyboardButton('🌀 Сдаюсь 🌀')
        markup.add(b_lox)
        msg = bot.send_message(message.chat.id, 'Введите число: ', reply_markup=markup)
        bot.register_next_step_handler(msg, process_game_proverka)
    else:
        sticker = open('AnimSticker.tgs', 'rb')
        bot.send_sticker(message.chat.id, sticker)
        send_welcome(message)


def process_game_proverka(message):
    chat_id = message.chat.id
    number = message.text
    if number == '🌀 Сдаюсь 🌀':
        sticker = open('lox.webp', 'rb')
        bot.send_sticker(chat_id, sticker)
        game(message)
    else:
        vivod = proverka_chisla(number=number)
        if _my_number[0] == list(number):
            bot.send_message(chat_id, f'{vivod}\n\nМууу! Победа!')
            send_welcome(message)
        else:
            msg = bot.send_message(chat_id, f'{vivod}\n\nВведите число: ')
            bot.register_next_step_handler(msg, process_game_proverka)


@bot.message_handler(commands=['exit'])
def exit(message):
    sticker = open('sticker2.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)


@bot.message_handler(commands=['draw'])
def draw(message):
    msg = bot.send_message(message.chat.id, 'Введите фразу')
    bot.register_next_step_handler(msg, draw_now)


def draw_now(message):
    chat_id = message.chat.id
    draw_mem = PostCardMaker(mem=message.text)
    mem_addr = f'mem_{message.from_user.first_name}_{message.date}.jpg'
    draw_mem.make(out_path=mem_addr)
    photo = open(f'C:\\Python\\Projects\\tg_bot\\draw\\pictures\\{mem_addr}', 'rb')
    bot.send_photo(chat_id, photo)
    send_welcome(message)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == "✏️ Добавить задачу ✏️":
        add(message)
    elif message.text == "📝 Посмотреть задачи 📝":
        show(message)
    elif message.text == "👁‍🗨 Магическая задача 👁‍🗨":
        random_add(message)
    elif message.text == "🫡 Попрощаться 🫡":
        exit(message)
    elif message.text == "🎮 Поиграем? 🎮":
        game(message)
    elif message.text == "🖼 Творим 🖼":
        draw(message)
    elif message.text == "🙏🏻 Информация 🙏🏻":
        help(message)
    else:
        bot.reply_to(message, message.text)


bot.polling(none_stop=True)

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.infinity_polling()
