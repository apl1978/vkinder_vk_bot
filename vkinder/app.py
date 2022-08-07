import requests
from token_group import token_group
import vk_api 
from db.interface_db import add_favourites

vk = vk_api.VkApi(token=token_group)

URL = "https://api.vk.com/method/"
HOME_PAGE = "https://vk.com/id"


# Обрабатываем сообщение запроса
def request_handler(msg):
    msg = msg[5:].split(',')
    sex = int(msg[0])
    status = int(msg[1])
    from_ = int(msg[2])
    to = int(msg[3])
    city = msg[4]
    return sex, status, from_, to, city


#  Ищем id кандита соответствующего параметрам запроса
def search_candidates(id, token: str, sex: int, status: int, age_from: int, age_to: int, hometown: str) -> list:
    url = URL + "users.search"
    params = {
            "access_token": f"{token}",
            "count": "20",
            "sex": f"{sex}",
            "hometown": f"{hometown}",
            "status": f"{status}",
            "age_from": f"{age_from}",
            "age_to": f"{age_to}",
            "has_photo": "1",
            "v": "5.132"
            }
    try:
        res = requests.get(url, params=params).json()
        res = res["response"]["items"]
    except KeyError:
        return False 
    except requests.exceptions.ConnectionError:
        print( f"Соединение было прервано.")
    else:
        if res != []:
            id_list = []
            check_list = add_favourites(id)
            for item in res:
                if item["id"] in check_list:
                    return None
                else:
                    id_list.append(item["id"])
            return id_list
        else:
            return None

# Получаем список состоящий из адреса домашней стр. и адресов топовых фото
def get_photo_and_url(id, token) -> list:
    pass