#  ================ Frontend Часть ====================
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text, BaseStateGroup
import re
from token_set import bot_group_id, bot_token
from vkinder.db.interface_db import insert_new_user, is_found_exists, insert_new_found, add_favourites, view_favourites
from auxiliary_functions import search_people, best_photo, parse_date, calc_age, id_people, AGE, SEX, bp

vk = Bot(bot_token, bot_group_id)

# ======= Списки с данными о человеке ========
you_sex = []
you_age = []
you_city = []


class CreateAnketa(BaseStateGroup):
    SEARCH = 0
    NAME = 1
    INFO = 2
    INFO1 = 3
    INFO2 = 4
    INFO3 = 5


@vk.on.private_message(lev=["Начать поиск 🔎"])
async def create_anket(message: Message):
    user_info_sex = await vk.api.users.get(message.from_id, 'sex')
    user_info_bdate = await vk.api.users.get(message.from_id, 'bdate')
    user_info_city = await vk.api.users.get(message.from_id, 'city')

    if user_info_bdate[0].bdate is None or user_info_sex[0].sex is None or user_info_city[0].city is None:
        await message.answer(message=f"О тебе слишком мало информации, давай её немного заполним!", keyboard=(
            Keyboard(one_time=True, inline=False)
            .add(Text('Заполнить'), color=KeyboardButtonColor.POSITIVE)
        ))
        await vk.state_dispenser.set(message.peer_id, CreateAnketa.INFO)
        return "Давай заполним!"

    else:
        you_city.append(user_info_city[0].city.title)
        you_age.append(user_info_bdate[0].bdate)
        if str(user_info_sex[0].sex) == "BaseSex.male":
            SEX.append(1)
            await message.answer(
                message=f"Вот вся информация о тебе: \nПол: Мужской\nВозраст: {user_info_bdate[0].bdate}\nТвой город: {user_info_city[0].city.title}",
                keyboard=(
                    Keyboard(one_time=True, inline=False)
                    .add(Text('Да'), color=KeyboardButtonColor.POSITIVE)
                    .add(Text('Изменить'), color=KeyboardButtonColor.POSITIVE)))
        else:
            SEX.append(2)
            await message.answer(
                message=f"Вот вся информация о тебе: \nПол: Женский\nВозраст:{user_info_bdate[0].bdate}\nТвой город:{user_info_city[0].city.title}",
                keyboard=(
                    Keyboard(one_time=True, inline=False)
                    .add(Text('Да'), color=KeyboardButtonColor.POSITIVE)
                    .add(Text('Изменить'), color=KeyboardButtonColor.POSITIVE)))
        await vk.state_dispenser.set(message.peer_id, CreateAnketa.SEARCH)
        return "Всё верно?"


@vk.on.private_message(state=CreateAnketa.INFO)
async def anceta_name(message: Message):
    await message.answer(
        message="Выбери свой пол:",
        keyboard=(
            Keyboard(one_time=True, inline=False)
            .add(Text("Я парень"), color=KeyboardButtonColor.POSITIVE)
            .add(Text("Я девушка"), color=KeyboardButtonColor.POSITIVE)
        ))
    await vk.state_dispenser.set(message.peer_id, CreateAnketa.INFO1)
    return "Поиск партнёров будет по противоположному полу"


@vk.on.private_message(state=CreateAnketa.INFO1)
async def anceta_name(message: Message):
    if message.text == "Я парень":
        you_sex.append("Мужской")
        SEX.append(1)
        await vk.state_dispenser.set(message.peer_id, CreateAnketa.INFO2)
        return "Напиши свой возраст в таком формате: 12.5.2001"
    elif message.text == "Я девушка":
        you_sex.append("Женский")
        SEX.append(2)
        await vk.state_dispenser.set(message.peer_id, CreateAnketa.INFO2)
        return "Напиши свой возраст в таком формате: 12.5.2001"
    else:
        await message.answer(message="Не коректно",
                             keyboard=(Keyboard(one_time=True, inline=False)
                                       .add(Text("Хорошо"), color=KeyboardButtonColor.POSITIVE)))
        await vk.state_dispenser.set(message.peer_id, CreateAnketa.INFO)
        return "Выбери пол из предложенного"


@vk.on.private_message(state=CreateAnketa.INFO2)
async def anceta_name(message: Message):
    age = re.findall(r"[0-9.]", message.text)
    if age == []:
        await vk.state_dispenser.set(message.peer_id, CreateAnketa.INFO2)
        return "Ты записал не в том формате (\nНадо так: 12.5.2001"
    else:
        you_age.append(message.text)
        await vk.state_dispenser.set(message.peer_id, CreateAnketa.INFO3)
        return "Отлично!\nТеперь запиши свой город!"


@vk.on.private_message(state=CreateAnketa.INFO3)
async def anceta_name(message: Message):
    city = re.findall(r"[а-яёА-ЯЁ-]", message.text)
    if city == []:
        await vk.state_dispenser.set(message.peer_id, CreateAnketa.INFO3)
        return f"Ты записал не в том формате\nЗапиши свой город на русском без пробелов и других символов"
    else:
        you_city.append(message.text)

        await message.answer(
            message=f"Вот вся информация о тебе: \nПол: {you_sex[-1]}\nВозраст: {you_age[-1]}\nТвой город: {message.text}",
            keyboard=(
                Keyboard(one_time=True, inline=False)
                .add(Text("Да"), color=KeyboardButtonColor.POSITIVE)
                .add(Text("Изменить"), color=KeyboardButtonColor.POSITIVE)))
        await vk.state_dispenser.set(message.peer_id, CreateAnketa.SEARCH)
        return f"Всё верно?"


@vk.on.private_message(state=CreateAnketa.SEARCH)
async def anceta_name(message: Message):
    AGE.append(calc_age(parse_date(f"{you_age[-1]}", fmt='%d.%m.%Y')))
    search_people(you_city[-1])

    if message.text == "Посмотреть ⭐":
        a = view_favourites(message.from_id)
        if a is None:
            return "Ваш список фаворитов пока пуст, добавьте кого-нибудь"
        else:
            for all in a:
                user_photo = await vk.api.users.get(all[0], "photo_id")

                photo_id = user_photo[0].photo_id

                await message.answer(message=f"""Имя Фамилия: {all[2]} {all[3]}
Ссылка на профиль: vk.com/id{all[0]}
Город: {all[6]}
Возраст: {all[4]}""",
                    attachment=f"photo{photo_id}")

            await vk.state_dispenser.set(message.peer_id, CreateAnketa.SEARCH)
            return "👎-пропустить\n⭐-добавить в избранное"

    elif message.text == "👎" or message.text.upper() == "ДА" or message.text == "⭐":
        if is_found_exists(message.from_id, id_people[0]) is None:
            user_name = await vk.api.users.get(id_people[0])
            user_age = await vk.api.users.get(id_people[0], "bdate")
            user_sex = await vk.api.users.get(id_people[0], "sex")
            user_city = await vk.api.users.get(id_people[0], "city")

            if len(user_age[0].bdate) >= 8:
                people_age = int(calc_age(parse_date(f"{user_age[0].bdate}", fmt='%d.%m.%Y')))
            else:
                people_age = 0

            if user_city[0].city is None:
                insert_new_found(message.from_id, id_people[0], user_name[0].first_name, user_name[0].last_name,
                                 people_age, user_sex[0].sex, "")
            else:
                insert_new_found(message.from_id, id_people[0], user_name[0].first_name, user_name[0].last_name,
                                 people_age, user_sex[0].sex, user_city[0].city.title)

            if message.text == "⭐":
                add_favourites(message.from_id, id_people[0])
            best_photo(user_name[0].id)
            # ========== Поиск пользователей ============
            await message.answer(message=f"""
Имя Фамилия: {user_name[0].first_name} {user_name[0].last_name}
Ссылка на профиль: vk.com/id{id_people[0]}""",
                 keyboard=(Keyboard(one_time=False, inline=False)
                           .add(Text('👎'), color=KeyboardButtonColor.NEGATIVE)
                           .add(Text('⭐'), color=KeyboardButtonColor.POSITIVE)
                           .row()
                           .add(Text('Посмотреть ⭐'), color=KeyboardButtonColor.POSITIVE)))
            for id_photo in bp[0]:
                await message.answer(attachment=f"photo{user_name[0].id}_{id_photo}")
            await vk.state_dispenser.set(message.peer_id, CreateAnketa.SEARCH)
            id_people.pop(0), bp.pop()
            return "👎-пропустить\n⭐-добавить в избранное"
        else:
            id_people.pop(0)
            while is_found_exists(message.from_id, id_people[0]) is not None:
                id_people.pop(0)
            await message.answer(message="Идёт поиск!",
                                 keyboard=(Keyboard(one_time=False, inline=False)
                                           .add(Text('ДА'), color=KeyboardButtonColor.POSITIVE)))
            await vk.state_dispenser.set(message.peer_id, CreateAnketa.SEARCH)
            return "Нажми ДА для продолжения"

    elif message.text == "Изменить":
        await message.answer(
            message=f"Выбери свой пол:",
            keyboard=(
                Keyboard(one_time=True, inline=False)
                .add(Text("Я парень"), color=KeyboardButtonColor.POSITIVE)
                .add(Text("Я девушка"), color=KeyboardButtonColor.POSITIVE)
            ))
        await vk.state_dispenser.set(message.peer_id, CreateAnketa.INFO1)
        id_people.pop()
        return "Поиск партнёров будет по противоположному полу"

    else:
        await message.answer(message="Я не знаю такой команды(", keyboard=(
            Keyboard(one_time=False, inline=False)
            .add(Text('👎'), color=KeyboardButtonColor.NEGATIVE)
            .add(Text('⭐'), color=KeyboardButtonColor.POSITIVE)
            .row()
            .add(Text('Посмотреть ⭐'), color=KeyboardButtonColor.POSITIVE)))
        await vk.state_dispenser.set(message.peer_id, CreateAnketa.SEARCH)
        return "Выбери команду из предложанных"


# ==========================================================
# ====================== ПРИВЕТСТВИЕ =======================
# ==========================================================
@vk.on.private_message(text=['Начать', 'Привет', "a"])
async def menu(message: Message):
    insert_new_user(message.from_id)
    await message.answer(
        message="Привет, найди себе кого-нибудь🤭",
        keyboard=(Keyboard(one_time=False, inline=False)
                  .add(Text('Начать поиск 🔎'), color=KeyboardButtonColor.SECONDARY)))


vk.run_forever()
