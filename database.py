import sqlite3
from config import MAX_USERS, DB_NAME, TABLE_NAME


class Database:
    def __init__(self, db_name=DB_NAME, table_name=TABLE_NAME):
        self.db_name = db_name
        self.table_name = table_name
        self.create_db_table()

    def create_db_table(self):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()

        query = """
        CREATE TABLE IF NOT EXISTS prompts(
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        role TEXT,
        content TEXT,
        date TEXT,
        tokens INTEGER,
        session_id INTEGER,
        genre TEXT,
        hero TEXT,
        setting TEXT
        );
        """

        cur.execute(query)
        con.commit()
        con.close()

    def execute_selection_query(self, sql_query, data=None):
        """
        Выполняет запрос sql_query с параметрами data и возвращает результат
        """
        con = sqlite3.connect("db.sqlite")  # устанавливаем соединение с БД
        cur = con.cursor()
        if data:
            cur.execute(sql_query, data)
        else:
            cur.execute(sql_query)
        rows = cur.fetchall()
        con.close()
        return rows

    def update_data(self, user_id, column, value):
        """
        Обновляет данные для пользователя user_id в столбце column, устанавливая значение value
        """

        con = sqlite3.connect(self.db_name)  # устанавливаем соединение с БД
        cur = con.cursor()  # создаём объект для работы с БД

        # формируем запрос UPDATE, в который подставляем название поля через f-строку
        # и значения через параметр ?
        sql_query = f"UPDATE prompts SET {column} = ? WHERE user_id = ?;"
        cur.execute(
            sql_query,
            (
                value,
                user_id,
            ),
        )  # применяем запрос и подставляем значения
        con.commit()  # сохраняем изменения в базе данных
        con.close()  # закрываем соединение с БД

    def is_limit_users(self):
        """
        Проверяет количество уникальных пользователей в БД
        """
        result = self.execute_selection_query(
            "SELECT COUNT(DISTINCT user_id) FROM prompts;"
        )

        return result[0][0] >= MAX_USERS

    def get_data(self, user_id):
        """
        Возвращает данные для пользователя user_id из БД
        """
        sql_query = "SELECT role, content, tokens, session_id, genre, hero, setting from prompts where user_id = ? limit 1"
        if len(list(self.execute_selection_query)) > 0:
            row = self.execute_selection_query(sql_query, [user_id])[-1]
            return {
                "role": row[0],
                "content": row[1],
                "tokens": row[2],
                "session_id": row[3],
                "genre": row[4],
                "hero": row[5],
                "setting": row[6],
                 }
        else:
            print("Что-то пошло не так")
