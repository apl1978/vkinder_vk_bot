from datetime import datetime
import vk_api
from token_set import api_token

# ================================================================
# =================== Поиск людей по критериям ===================
# ================================================================
vks = vk_api.VkApi(token=api_token)
api = vks.get_api()
id_people = []
AGE = []
SEX = []


def search_people(city):
    rs = api.users.search(hometown=city, age_from=int(AGE[-1]) - 1, age_to=int(AGE[-1]) + 1, fields='is_closed',
                          count=1000, sex=SEX[-1], has_photo=1)
    users_ids = [user['id'] for user in rs['items']]
    is_closed = [user['is_closed'] for user in rs['items']]
    i = 0
    for ids in users_ids:
        if is_closed[i] == False:
            id_people.append(ids)
        i += 1


# ===================================================
# =========== ТРИ ЛУЧШИХ ФОТО С ПРОФИЛЯ =============
# ===================================================
bp = []


def best_photo(id_profile):
    photo_info = api.photos.get(album_id="profile", owner_id=id_profile, extended=1)
    idPhoto_like = {}
    for photo in photo_info["items"]:
        idPhoto_like[str(photo["id"])] = int(photo["likes"]['count'])
    bp.append(sorted(idPhoto_like, key=idPhoto_like.get, reverse=True)[:3])


# =====================================
# =========== сколько лет =============
# =====================================
def parse_date(s, fmt='%d/%m/%Y'):
    d = s.split()[0]
    return datetime.strptime(d, fmt)


def calc_age(d):
    today = datetime.today()
    return today.year - d.year - ((today.month, today.day) < (d.month, d.day))
