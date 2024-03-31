"""
Основной исполняемый скрипт-файл
"""

import logging
import time

from telebot import TeleBot

from config import BOT_TOKEN, MAX_SESSIONS, LOG_FILE_PATH
from database import Database
from gpt import GPT
from statics import get_genre_keyboard, get_hero_keyboard, get_setting_keyboard


bot = TeleBot(token=BOT_TOKEN)
db = Database()
gpt = GPT()
'''
token_data = gpt.create_new_token()
expires_at = time.time() + token_data["expires_in"]
if expires_at < time.time():
    gpt.create_new_token()
'''
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=LOG_FILE_PATH,
    filemode="a",
)


@bot.message_handler(commands=["start"])
def start_command(message):
    user_name = message.from_user.first_name
    bot.send_message(message.from_user.id, text=f"Приветствую тебя, {user_name}!")
    db.create_db_table()


@bot.message_handler(commands=["help"])
def help_command(message):
    bot.send_message(
        message.from_user.id,
        text="Я твой цифровой собеседник 👾 Узнать обо мне подробнее можно командой /about",
    )


@bot.message_handler(commands=["about"])
def about_command(message):
    bot.send_message(
        message.from_user.id,
        text="Рад, что ты заинтересован_а! Мое предназначение — не оставлять тебя в одиночестве и всячески подбадривать! 🤍🤍"
        " С помощью GPT составлю с тобой сценарий. Нажмите кнопку /create, чтобы начать "
        "создание истории, /continue - продолжить, /end - увидеть конец, а также все получившееся."
        " Пожалуйста, не вводите очень длинные сообщения, стоит ограничение на ввод 🖤",
    )


@bot.message_handler(commands=["debug"])
def send_logs(message):
    with open("log_file.txt", "rb") as f:
        bot.send_document(message.chat.id, f)


@bot.message_handler(commands=["create"])
def create_story(message):
    sessions_id = 0
    sessions_id += 1
    if db.is_limit_users():
        bot.send_message(
            message.from_user.id,
            text="Лимит пользователей исчерпан",
        )
        return

    if sessions_id < MAX_SESSIONS:
        bot.send_message(
            message.from_user.id,
            text="Для начала выбери жанр своей истории",
            reply_markup=get_genre_keyboard(),
        )
        bot.register_next_step_handler(message, choose_genre)
    else:
        bot.send_message(message.from_user.id, text="Лимит сессий исчерпан")


def choose_genre(message):
    GENRES = ["Комедия", "Фантастика", "Драма"]
    if message.text not in GENRES:
        bot.send_message(
            message.chat.id,
            "Пожалуйста, выберите жанр",
            reply_markup=get_genre_keyboard(),
        )
        bot.register_next_step_handler(message, choose_genre)
        return

    db.update_data(message.from_user.id, "genre", message.text)

    bot.send_message(
        message.from_user.id,
        text="Выбери персонажа своей истории",
        reply_markup=get_hero_keyboard(),
    )

    bot.register_next_step_handler(message, choose_hero)


def choose_hero(message):
    HEROES = ["Серена ван дер Вудсен", "Блэр Уолдорф", "Человек-паук", "Кот Маркус"]
    if message.text not in HEROES:
        bot.send_message(
            message.from_user.id,
            text="Выбери персонажа своей истории",
            reply_markup=get_hero_keyboard(),
        )
        bot.register_next_step_handler(message, choose_hero)
        return

    db.update_data(message.from_user.id, "hero", message.text)

    bot.send_message(
        message.from_user.id,
        text="Выбери сеттинг для своей истории",
        reply_markup=get_setting_keyboard(),
    )

    bot.register_next_step_handler(message, choose_setting)


def choose_setting(message):
    SETTINGS = [
        "Нью-Йорк - город контрастов",
        "Санкт-Петербург - город наш",
        "Вселенная 2041",
        "Царство Филори",
    ]

    if message.text not in SETTINGS:
        bot.send_message(
            message.from_user.id,
            text="Выбери сеттинг для своей истории",
            reply_markup=get_hero_keyboard(),
        )
        bot.register_next_step_handler(message, choose_setting)
        return

    db.update_data(message.from_user.id, "setting", message.text)

    bot.send_message(message.chat.id, "Укажи что еще хочешь учесть в сценарии")
    bot.register_next_step_handler(message, add_info)


def add_info(message):
    user_id = message.from_user.id

    helper_prompt = message.text
    db.update_data(user_id, "content", helper_prompt)

    bot.send_message(message.chat.id, "Все учтем!")
    user_info = db.get_data(message.from_user.id)

    mode = "create"

    gpt.ask_gpt(user_info, helper_prompt, mode, user_id)

    # TODO - Сделать реакцию на ответ от GPT - потльзователь может продолжить генерацию текста, а может и прервать генерацию начав новую сессию

@bot.message_handler(commands=['continue_explaining'])
def continue_explaining(message):
    user_id = message.from_user.id
    mode = "continue"
    gpt.ask_gpt(user_id, mode)


@bot.message_handler(commands=['end'])
def end(message):
    user_id = message.from_user.id
    mode = "end"
    gpt.ask_gpt(user_id, mode)


bot.polling()
