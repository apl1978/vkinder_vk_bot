from typing import NoReturn, Tuple, Optional

import psycopg2
import configparser

config = configparser.ConfigParser()
if __name__ == '__main__':
    config.read("settings_db.ini")
else:
    config.read(".\db\settings_db.ini")

HOST = config["DB"]["host"]
PORT = config["DB"]["port"]
DATABASE = config["DB"]["database"]
USER = config["DB"]["user"]
PASSWORD = config["DB"]["password"]


def _cursor_execute(sql_str: str, t_params: Tuple, commit: bool) -> Optional[Tuple]:
    conn = psycopg2.connect(host=HOST, port=PORT, database=DATABASE, user=USER, password=PASSWORD)

    result = None
    with conn.cursor() as cur:
        cur.execute(sql_str, t_params)
        if commit:
            conn.commit()
        else:
            result = cur.fetchone()
    conn.close()
    return result


def insert_new_user(user_id: int) -> NoReturn:
    sql_str = 'SELECT user_id FROM users WHERE user_id =%s'
    t_params = (user_id,)
    result = _cursor_execute(sql_str, t_params, False)

    if result is None:
        sql_str = 'INSERT INTO users (user_id) VALUES (%s)'
        t_params = (user_id,)
        _cursor_execute(sql_str, t_params, True)


def is_found_exists(user_id: int, found_id: int) -> Optional[Tuple]:
    result = None
    sql_str = 'SELECT found_id FROM found WHERE user_id =%s and found_id =%s'
    t_params = (user_id, found_id)
    result = _cursor_execute(sql_str, t_params, False)
    return result


def insert_new_found(user_id: int, found_id: int, first_name: str, last_name: str, age: int, gender: str, city: str) -> NoReturn:
    result = is_found_exists(user_id, found_id)

    if result is None:
        sql_str = 'INSERT INTO found (user_id, found_id, first_name, last_name, age, gender, city) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        t_params = (user_id, found_id, first_name, last_name, age, gender, city)
        _cursor_execute(sql_str, t_params, True)
