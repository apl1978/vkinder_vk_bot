from typing import NoReturn, Tuple, Optional, List
import psycopg2
import configparser
import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS_DIR_NAME = 'db'
SETTINGS_FILE_NAME = 'settings_db.ini'

file_path = os.path.join(BASE_PATH, SETTINGS_DIR_NAME, SETTINGS_FILE_NAME)
config = configparser.ConfigParser()
config.read(file_path)

HOST = config["DB"]["host"]
PORT = config["DB"]["port"]
DATABASE = config["DB"]["database"]
USER = config["DB"]["user"]
PASSWORD = config["DB"]["password"]


def _cursor_execute(sql_str: str, t_params: Tuple, commit: bool) -> Optional[List]:
    conn = psycopg2.connect(host=HOST, port=PORT, database=DATABASE, user=USER, password=PASSWORD)

    result = None
    with conn.cursor() as cur:
        cur.execute(sql_str, t_params)
        if commit:
            conn.commit()
        else:
            t_result = cur.fetchall()
            if t_result:
                result = t_result
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


def is_found_exists(user_id: int, found_id: int) -> Optional[List]:
    result = None
    sql_str = 'SELECT found_id FROM found WHERE user_id =%s and found_id =%s'
    t_params = (user_id, found_id)
    result = _cursor_execute(sql_str, t_params, False)
    return result


def insert_new_found(user_id: int, found_id: int, first_name: str, last_name: str, age: int, gender: str,
                     city: str) -> NoReturn:
    result = is_found_exists(user_id, found_id)

    if result is None:
        sql_str = 'INSERT INTO found (user_id, found_id, first_name, last_name, age, gender, city) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        t_params = (user_id, found_id, first_name, last_name, age, gender, city)
        _cursor_execute(sql_str, t_params, True)


def add_favourites(user_id: int, found_id: int) -> NoReturn:
    sql_str = 'SELECT user_id, found_id FROM favourites WHERE user_id =%s and found_id =%s'
    t_params = (user_id, found_id)
    result = _cursor_execute(sql_str, t_params, False)

    if result is None:
        sql_str = 'INSERT INTO favourites (user_id, found_id) VALUES (%s, %s)'
        t_params = (user_id, found_id)
        _cursor_execute(sql_str, t_params, True)


def view_favourites(user_id: int) -> Optional[List]:
    result = None
    sql_str = '''
    SELECT * FROM found AS f
    JOIN
    favourites AS fav
    ON f.user_id = fav.user_id AND f.found_id = fav.found_id
    WHERE f.user_id = %s
    '''

    t_params = (user_id,)
    result = _cursor_execute(sql_str, t_params, False)
    return result
