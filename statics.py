from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def get_genre_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Комедия"))
    markup.add(KeyboardButton("Фантастика"))
    markup.add(KeyboardButton("Драма"))


def get_hero_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Серена ван дер Вудсен"))
    markup.add(KeyboardButton("Блэр Уолдорф"))
    markup.add(KeyboardButton("Человек-паук"))
    markup.add(KeyboardButton("Кот Маркус"))


def get_setting_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Нью-Йорк - город контрастов"))
    markup.add(KeyboardButton("Санкт-Петербург - город наш"))
    markup.add(KeyboardButton("Вселенная 2041"))
    markup.add(KeyboardButton("Царство Филори"))
