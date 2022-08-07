import requests
from token_group import token_group
import vk_api 

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
    pass

# Получаем список состоящий из адреса домашней стр. и адресов топовых фото
def get_photo_and_url(id, token) -> list:
    pass