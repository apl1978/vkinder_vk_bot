import requests
from token_group import token_group
import vk_api

vk = vk_api.VkApi(token=token_group)

URL = "https://api.vk.com/method/"
HOME_PAGE = "https://vk.com/id"


# Обрабатываем сообщение запроса
def request(msg):
    pass


# Ищем id кандита соответствующего параметрам запроса
def search_candidates(id):
    pass


# Получаем список состоящий из адреса домашней стр. и адресов топовых фото
def get_photo_and_url(id, token) -> list:
    pass