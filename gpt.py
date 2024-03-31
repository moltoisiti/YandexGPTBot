"""
Модуль для работы с YandexGPT
"""

import requests

from config import (
    MAX_PROJECT_TOKENS,
    IAM_TOKEN,
    FOLDER_ID,
    URL_TOKENIZE,
    URL_COMPLETION,
    REQUEST_TIMEOUT_SECONDS,
    IAM_TOKEN_REFRESH,
)
#from bot import db
from database import Database
db = Database()


# Подсчитывает количество токенов в тексте
class GPT:
    """
    Класс для работы с YandexGPT
    """

    def count_tokens(self, text):
        """
        Функция подсчета количества токенов в тексте
        """

        headers = {  # заголовок запроса, в котором передаем IAM-токен
            "Authorization": f"Bearer {IAM_TOKEN}",  # token - наш IAM-токен
            "Content-Type": "application/json",
        }
        data = {
            "modelUri": f"gpt://{FOLDER_ID}/yandexgpt/latest",  # указываем folder_id
            "maxTokens": MAX_PROJECT_TOKENS,
            "text": text,  # text - тот текст, в котором мы хотим посчитать токены
        }
        try:
            return len(
                requests.post(
                    url=URL_TOKENIZE,
                    json=data,
                    headers=headers,
                    timeout=REQUEST_TIMEOUT_SECONDS,
                ).json()["tokens"]
            )  # здесь, после выполнения запроса, функция возвращает количество токенов в text
        except Exception:
            return MAX_PROJECT_TOKENS

    def ask_gpt(self, user_info_dict, user_prompr, mode, user_id):
        """
        Функция отвечающая за генерацию текста для пользователя
        """
        headers = {
            "Authorization": f"Bearer {IAM_TOKEN}",
            "Content-Type": "application/json",
        }

        genre = user_info_dict["genre"]
        hero = user_info_dict["hero"]
        setting = user_info_dict["setting"]
        if mode == "create":
            system_prompt = (
                f"Придумай сценарий в жанре {genre}, где главный герой {hero} находится в {setting}. Также учти пожелание пользователя:"
                f"{user_prompr}"
            )
            db.update_data(user_id, "content", system_prompt)
        elif mode == "continue":
            result = db.get_data(user_id)
            text = result["content"]
            system_prompt = (
                f"Придумай сценарий в жанре {genre}, где главный герой {hero} находится в {setting}. Также учти пожелание пользователя:"
                f"{user_prompr}. Начало ответа: {text}"
            )
            db.update_data(user_id, "content", system_prompt)
        else: #т.е. end
            result = db.get_data(user_id)
            text = result["content"]
            system_prompt = (
                f"Придумай неожиданную концовку в 1-2 предложения" + " Вот такая история получилась" +
                f"{text}"
            )
        result = db.get_data(user_id)

        text = result["content"]

        data = {
            "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-lite",  # модель для генерации текста
            "completionOptions": {
                "stream": False,  # потоковая передача частично сгенерированного текста выключена
                "temperature": "TEMPERATURE",  # чем выше значение этого параметра, тем более креативными будут ответы модели (0-1)
                "maxTokens": "MAX_TOKENS_QUE",  # максимальное число сгенерированных токенов, очень важный параметр для экономии токенов
            },
            "messages": [
                {
                    "role": "user",  # пользователь спрашивает у модели
                    "text": text,  # передаём текст, на который модель будет отвечать
                }
            ],
        }
        try:
            response = requests.post(
                url=URL_COMPLETION,
                headers=headers,
                json=data,
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
            text = response.json()["result"]["alternatives"][0]["message"]["text"]
            return text
        except Exception:
            return "Не удалось сгенерировать текст :("

    def create_new_token(self):
        """
        Создание нового токена
        """
        try:
            metadata_url = IAM_TOKEN_REFRESH
            headers = {"Metadata-Flavor": "Google"}
            response = requests.get(metadata_url, headers=headers)
            return response.json()
        except Exception:
            exit(1)
