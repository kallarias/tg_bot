import random
import telebot
import time
import logging

from pony.orm import db_session
from telebot import types
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

from draw.draw_mem import PostCardMaker
from mastermind_engine import FourBulls
from models import UserTasks

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
flag = 0
bot_help = settings.HELP_INFO
user_dict = {}
random_task = settings.RANDOM_THINGS
tconv = lambda x: time.strftime("%H:%M:%S %Y-%m-%d", time.localtime(x))  # Конвертация даты в читабельный вид
configure_logging()
bot.set_my_commands(settings.BOT_MENU_CONFIG)
shag = 0


@db_session
def add_db(user_id, name, data, task):
    UserTasks(user_id=user_id,
              name=name,
              date=data,
              task=task)


class AddTasks:
    def __init__(self, name):
        self.name = name
        self.data = None
        self.task = None
        self.flag = 0
        self.user_id = 0
        self.game = None


def add_user(message, user_flag=0, game=False):
    chat_id = message.chat.id
    name = message.from_user.first_name
    user = AddTasks(name)
    user_dict[chat_id] = user
    user_id = message.from_user.id
    add_id = user_dict[chat_id]
    add_id.user_id = user_id
    add_id.flag = user_flag
    if game:
        add_id.game = FourBulls(user_id=message.from_user.id)


@bot.message_handler(commands=['start'])
def send_welcome(message):
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
def f_help(message):
    markup = types.InlineKeyboardMarkup()
    switch_button = types.InlineKeyboardButton(text='Порекомендовать бота',
                                               switch_inline_query="Думаю ты не разочаруешься")
    markup.add(switch_button)
    bot.send_message(message.chat.id, bot_help, reply_markup=markup)


@bot.message_handler(commands=['add'])
def add(message):
    add_user(message=message, user_flag=1)
    calendar, step = DetailedTelegramCalendar().build()
    bot.send_message(message.chat.id,
                     f"Select {LSTEP[step]}",
                     reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(call):
    result, key, step = DetailedTelegramCalendar().process(call.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:
        chat_id = call.message.chat.id
        user_info = user_dict[chat_id]
        data = str(result)
        if user_info.flag == 1:
            try:
                user_info.data = data
                msg = bot.edit_message_text(f"Вы выбрали {result}\nВведите задачу: ",
                                            chat_id,
                                            call.message.message_id)
                bot.register_next_step_handler(msg, process_sex_step)
            except Exception as e:
                bot.reply_to(call.message, e)
        elif user_info.flag == 2:
            try:
                text = ""
                task = db_catch(data=data, user_id=user_info.user_id)
                if len(task) > 0:
                    text = "Планы на дату: " + data.upper()
                    for p in task:
                        text = f'{text}\n❗️ {p.task} '
                else:
                    text = data.upper()
                    text = "На дату " + text + "\nДанных нет!"
                bot.edit_message_text(text, chat_id, call.message.message_id)
            except Exception as e:
                bot.reply_to(call.message, e)
        user_info.flag = 0


@db_session
def db_catch(data, user_id):
    task = UserTasks.select_by_sql(
        "SELECT * FROM UserTasks p WHERE p.date = $data AND p.user_id = $user_id")
    return task


def process_sex_step(message):
    try:
        chat_id = message.chat.id
        task = message.text
        add_tasks = user_dict[chat_id]
        add_tasks.task = task
        add_db(user_id=message.from_user.id, name=add_tasks.name, data=add_tasks.data, task=add_tasks.task)
        bot.send_message(chat_id, 'Добрый день ' + add_tasks.name + '\nЗадача ' + str(
            add_tasks.task) + ' записана на ' + add_tasks.data)
        log.info(f"Добавлена задача для пользователя {message.from_user.id}")
    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(commands=['show'])
def show(message):
    add_user(message=message, user_flag=2)
    calendar, step = DetailedTelegramCalendar().build()
    bot.send_message(message.chat.id,
                     f"Select {LSTEP[step]}",
                     reply_markup=calendar)


@bot.message_handler(commands=['random'])
def random_add(message):
    task = random.choice(random_task)
    data1 = tconv(message.date)
    command = data1.split()
    data = command[1]
    add_db(user_id=message.from_user.id, name=message.from_user.first_name, data=data, task=task)
    bot.send_message(message.chat.id,
                     'Добрый день ' + message.from_user.first_name + '\nЗадача ' + task + ' записана на ' + data)


@bot.message_handler(commands=['game'])
def game(message):
    add_user(message=message, game=True)
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
    except Exception as exp:
        bot.reply_to(message, exp)


def process_game(message):
    if message.text == '✅ Да ✅':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        b_lox = types.KeyboardButton('🌀 Сдаюсь 🌀')
        markup.add(b_lox)
        msg = bot.send_message(message.chat.id, 'Введите число: ', reply_markup=markup)
        bot.register_next_step_handler(msg, process_game_proverka)
    else:
        sticker = open('images/AnimSticker.tgs', 'rb')
        bot.send_sticker(message.chat.id, sticker)
        send_welcome(message)


def process_game_proverka(message):
    chat_id = message.chat.id
    number = message.text
    if number == '🌀 Сдаюсь 🌀':
        sticker = open('images/lox.webp', 'rb')
        bot.send_sticker(chat_id, sticker)
        game(message)
    else:
        global shag
        shag += 1
        chat_id = message.chat.id
        user_info = user_dict[chat_id]
        vivod = user_info.game.proverka_chisla(number=number)
        _my_number = user_info.game.return_number()
        log.info(f"загаданное число {_my_number[0]}")
        if _my_number[0] == list(number):
            bot.send_message(chat_id, f'{vivod}\n\nМууу! Победа!\n Вы угадали число за {shag} шагов!')
            shag = 0
            _my_number.clear()
            send_welcome(message)
        else:
            msg = bot.send_message(chat_id, f'{vivod}\n\nВведите число: ')
            bot.register_next_step_handler(msg, process_game_proverka)


@bot.message_handler(commands=['exit'])
def bot_exit(message):
    sticker = open('images/sticker2.webp', 'rb')
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


@bot.message_handler(commands=['anime'])
def anime(message):
    markup = types.InlineKeyboardMarkup()
    btn_my_site = types.InlineKeyboardButton(text='Секретный уголок', url='https://shikimori.one/Jskoo')
    markup.add(btn_my_site)
    bot.send_message(message.chat.id, "Попробуй посмотри их все!", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == "✏️ Добавить задачу ✏️":
        add(message)
    elif message.text == "📝 Посмотреть задачи 📝":
        show(message)
    elif message.text == "👁‍🗨 Магическая задача 👁‍🗨":
        random_add(message)
    elif message.text == "🫡 Попрощаться 🫡":
        bot_exit(message)
    elif message.text == "🎮 Поиграем? 🎮":
        game(message)
    elif message.text == "🖼 Творим 🖼":
        draw(message)
    elif message.text == "🙏🏻 Информация 🙏🏻":
        f_help(message)
    else:
        bot.reply_to(message, message.text)


bot.polling(none_stop=True)

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will happen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.infinity_polling()
