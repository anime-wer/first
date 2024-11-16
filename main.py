from config import TOKEN
import telebot
from telebot.types import Message, ReplyKeyboardMarkup as rkm, InlineKeyboardMarkup as ikm, InlineKeyboardButton as ikb, \
    CallbackQuery
import time

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["inline"])
def inline(m: Message):
    kb = ikm()
    kb.row(ikb("точно не вычислю по айпи", url="https://yandex.ru"),
           ikb("точно не вычислю по айпи", url="https://www.google.ru"))
    kb.row(ikb("точно не вычислю по айпи", url="https://www.youtube.com"),
           ikb("кнопка", callback_data="BTN"))
    kb.row(ikb("oodaj", callback_data="ops"))
    bot.send_message(m.chat.id, "вы лох", reply_markup=kb)


@bot.message_handler(commands=["register"])
def register(m: Message):
    bot.send_message(m.chat.id, "первый регистрационный вопрос, как тебя назвала ваша семья при вашем рождении?")
    bot.register_next_step_handler(m, reg1)


def reg1(m: Message):
    name = m.text
    bot.send_message(m.chat.id, f"{name}, сколько тебе лет?")
    bot.register_next_step_handler(m, reg2, name)


def reg2(m: Message, name):
    age = m.text
    bot.send_message(m.chat.id, f"{name} тебе {age}, где ты живёшь?")
    bot.register_next_step_handler(m, reg3, name, age)


def reg3(m: Message, name, age):
    town = m.text
    bot.send_message(m.chat.id, f"{name} тебе {age} ты живёшь в городе {town}, твой любимый цвет?")


@bot.callback_query_handler(func=lambda call: True)
def callback(call: CallbackQuery):
    print(call.data)
    if call.data == "BTN":
        start(call.message)
    elif call.data == "ops":
        bot.send_message(call.message.chat.id, "rur")


@bot.message_handler(commands=["start"])
def start(m: Message):
    user_id = m.chat.id
    print(f"{m.from_user.full_name} - id: {user_id}")
    bot.send_message(m.chat.id, f"привет {m.from_user.first_name} {m.from_user.last_name}, кинь координаты "
                                f"чтоб навести на тебя артиллерию")


@bot.message_handler(commands=["user_enter"])
def user_enter(m: Message):
    bot.reply_to(m, "ты что то знаешь...")
    bot.send_message(5387128635, f"в бота написал {m.from_user.full_name} - id: {m.chat.id}")


@bot.message_handler(commands=["help"])
def help(m: Message):
    kb = rkm(resize_keyboard=True, one_time_keyboard=True)
    kb.row("/start", "/help")
    kb.row("привет")
    bot.reply_to(m, "есть 3 команды\n/start\n/user_enter\n/help", reply_markup=kb)
    bot.send_message(5387128635, f"в бота написал {m.from_user.full_name}\nid: {m.chat.id} "
                                 f"\nпервое имя которого {m.from_user.first_name}\nпремиум{m.from_user.is_premium}")


@bot.message_handler(content_types=["text"])
def text(m: Message):
    msg = m.text.lower()
    if msg == "анан":
        print("какой тфа дэбил написал")
        bot.reply_to(m, "ты дураак?")
        time.sleep(2)
        help(m)
    elif msg == "привет":
        bot.send_message(m.chat.id, "че хотел?")


@bot.message_handler(content_types=["audio"])
def audio(m: Message):
    sound = m.audio
    durex = f"{sound.duration // 60} min {sound.duration % 60} secks"
    txt = f"бот получил аудио\n{sound.performer} - {sound.title}\n{durex}\n{round(sound.file_size / 1024 ** 2, 2)}мб"
    print(txt)
    bot.send_message(m.chat.id, txt)
    file_id = sound.file_id
    file_info = bot.get_file(file_id)
    download_file = bot.download_file(file_info.file_path)
    with open(f"{sound.performer} - {sound.title}.mp3", "wb") as file:
        file.write(download_file)
    bot.reply_to(m, "аудио скачано")


@bot.message_handler(content_types=["photo"])
def handle_docs_photo(m: Message):
    file_id = m.photo[-1].file_id
    print(file_id)
    file_info = bot.get_file(file_id)
    print(file_info)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(f"{file_info.file_unique_id}.jpg", "wb") as new_file:
        new_file.write(downloaded_file)


bot.infinity_polling()
