#  ================ Frontend Часть ====================
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text, BaseStateGroup, CtxStorage, PhotoMessageUploader
import re

from token_set import bot_group_id, bot_token

from vkinder.db.interface_db import insert_new_user



vk = Bot(bot_token, bot_group_id)

# ==========================================================
# =================== CОЗДАНИЕ АНКЕТЫ ======================
# ==========================================================
class CreateAnketa(BaseStateGroup):
    AGE = 0
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

        if user_info_bdate[0].bdate == None or user_info_sex[0].sex == None or user_info_city[0].city == None:
            await message.answer(message=f"О тебе слишком мало информации, давай её немного заполним!", keyboard=(
                    Keyboard(one_time=True, inline=False)
                    .add(Text('Заполнить'), color=KeyboardButtonColor.POSITIVE)
                ))
            await vk.state_dispenser.set(message.peer_id, CreateAnketa.INFO)
            return "Давай заполним!"

        else:
            you_city = "".join(re.findall(r"[а-яёА-ЯЁ-]", str(user_info_city[0].city)))

            if str(user_info_sex[0].sex) == "BaseSex.male":
                await message.answer(message=f"Вот вся информация о тебе: \nПол: Мужской\nВозраст: {user_info_bdate[0].bdate}\nТвой город: {you_city}", keyboard=(
                        Keyboard(one_time=True, inline=False)
                        .add(Text('Да'), color=KeyboardButtonColor.POSITIVE)
                        .add(Text('Изменить'), color=KeyboardButtonColor.POSITIVE)
                    ))
                await vk.state_dispenser.set(message.peer_id, CreateAnketa.AGE)
                return "Всё верно?"
            else:
                await message.answer(message=f"Вот вся информация о тебе: \nПол: Женский\nВозраст:{user_info_bdate[0].bdate}\nТвой город:{you_city}", keyboard=(
                        Keyboard(one_time=True, inline=False)
                        .add(Text('Да'), color=KeyboardButtonColor.POSITIVE)
                        .add(Text('Изменить'), color=KeyboardButtonColor.POSITIVE)
                    ))
                await vk.state_dispenser.set(message.peer_id, CreateAnketa.AGE)
                return "Всё верно?"


@vk.on.private_message(state=CreateAnketa.INFO)
async def anceta_name(message: Message):
    await message.answer(
        message=f"Выбери свой пол:",
        keyboard=(
            Keyboard(one_time=True, inline=False)
            .add(Text("Я парень"), color=KeyboardButtonColor.POSITIVE)
            .add(Text("Я девушка"), color=KeyboardButtonColor.POSITIVE)
        ))
    await vk.state_dispenser.set(message.peer_id, CreateAnketa.INFO1)
    return ")"

you_sex = []
you_age = []
you_city = []
@vk.on.private_message(state=CreateAnketa.INFO1)
async def anceta_name(message: Message):
    you_sex.append(message.text)

    await vk.state_dispenser.set(message.peer_id, CreateAnketa.INFO2)
    return "Напиши свой возраст в таком формате: 12.5.2001"

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
        await message.answer(
            message=f"Вот вся информация о тебе: \nПол: {you_sex[0]}\nВозраст: {you_age[0]}\nТвой город: {message.text}",
            keyboard=(
                Keyboard(one_time=True, inline=False)
                .add(Text("Да"), color=KeyboardButtonColor.POSITIVE)
                .add(Text("Изменить"), color=KeyboardButtonColor.POSITIVE)
            ))
        await vk.state_dispenser.set(message.peer_id, CreateAnketa.AGE)
        return f"Всё верно?"

@vk.on.private_message(state=CreateAnketa.AGE)
async def anceta_name(message: Message):
    if message.text == "⭐":
        """Сохраняем данные о человеке в БД"""

    elif message.text == "Посмотреть ⭐":
        """Выводим спок сохраённых людей"""

    elif message.text == "👎" or message.text.upper() == "ДА":
        """Показываем следующего человека"""

        await message.answer(message="""Имя Фамилия
        ссылка на профиль
        три фотографии в виде attachment(https://dev.vk.com/method/messages.send)""", keyboard=(
            Keyboard(one_time=False, inline=False)
            .add(Text('👎'), color=KeyboardButtonColor.NEGATIVE)
            .add(Text('⭐'), color=KeyboardButtonColor.POSITIVE)
            .row()
            .add(Text('Посмотреть ⭐'), color=KeyboardButtonColor.POSITIVE)
        ))
        await vk.state_dispenser.set(message.peer_id, CreateAnketa.AGE)
        return "👎-пропустить\n⭐-добавить в избранное"

    elif message.text == "Изменить":
        await message.answer(
            message=f"Выбери свой пол:",
            keyboard=(
                Keyboard(one_time=True, inline=False)
                .add(Text("Я парень"), color=KeyboardButtonColor.POSITIVE)
                .add(Text("Я девушка"), color=KeyboardButtonColor.POSITIVE)
            ))
        await vk.state_dispenser.set(message.peer_id, CreateAnketa.INFO1)
        return ")"

    else:
        await message.answer(message="Я не знаю такой команды(", keyboard=(
            Keyboard(one_time=False, inline=False)
            .add(Text('👎'), color=KeyboardButtonColor.NEGATIVE)
            .add(Text('⭐'), color=KeyboardButtonColor.POSITIVE)
            .row()
            .add(Text('Посмотреть ⭐'), color=KeyboardButtonColor.POSITIVE)
        ))
        await vk.state_dispenser.set(message.peer_id, CreateAnketa.AGE)
        return "Выбери команду из предложанных"

# ==========================================================
# ====================== ПРИВЕТСТВИЕ =======================
# ==========================================================
@vk.on.private_message(text=['Начать', 'Привет', "a"])
async def menu(message: Message):
    print(message.from_id)
    insert_new_user(message.from_id)
    await message.answer(
        message="Привет, найди себе кого-нибудь🤭",
        keyboard=(
            Keyboard(one_time=False, inline=False)
            .add(Text('Начать поиск 🔎'), color=KeyboardButtonColor.SECONDARY)
        )
    )

vk.run_forever()