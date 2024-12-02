from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from ai_bot.core.database.orm_query import put_access_token_db, get_access_token_db, get_all_users_db
from ai_bot.core.keyboards.keyboards import main_menu
from ai_bot.core.utils.BotStates import Register, Work

from ai_bot.core.api_tools.request_api import get_access_token

router_handler = Router()


# @router_handler.message()
# async def handle_photo(message: Message):
#     # Получение объекта фото
#     photo = message.video.
#     # Загрузка фото на ваш сервер
#     print(photo)
@router_handler.message(Command('start'))
async def get_start(message: Message, bot: Bot, state: FSMContext, session: AsyncSession):
    user_id = message.from_user.id
    all_users_id = [int(obj.user_id) for obj in await get_all_users_db(session)]

    await state.clear()

    if int(user_id) in all_users_id:
        await state.set_state(Work.main_menu)
        # print(await get_access_token_db(session, {"user_id": user_id}))

        text = """Выберете тип работы:"""

        await message.answer(text, reply_markup=main_menu)
        await state.set_state(Work.main_menu)
    else:
        await state.set_state(Register.login)
        text1 = """Приветствую вас, я бот проекта Кода Памяти. Моя цель состоит в том,чтобы создать фото- и видеоматериалы по биографии вашего родственника.
Пройдите авторизацию,чтобы продолжить."""
        await message.answer(text1)
        text2 = """Введите свой Email:"""
        await message.answer(text2)


# регистрация
@router_handler.message(Register.login)
async def get_login(message: Message, bot: Bot, state: FSMContext, session: AsyncSession):
    await state.update_data(login=message.text)
    await state.set_state(Register.password)
    await message.answer("Введите пароль:")


@router_handler.message(Register.password)
async def get_pass_login(message: Message, bot: Bot, state: FSMContext, session: AsyncSession):
    st_n = await state.get_data()

    login = st_n.get('login')
    password = message.text

    access_token = await get_access_token(login, password)
    print(access_token)
    if access_token:
        data = {
            "user_id": int(message.from_user.id),
            "access_token": access_token,
        }
        await put_access_token_db(session, data)

        all_users_id = [int(obj.user_id) for obj in await get_all_users_db(session)]
        print(all_users_id)
        await get_start(message, bot, state, session)
    else:
        await message.answer(
            """Данного пользователя не существует. Проверьте корректность данных или пройдите регистрацию на <a href="https://mc.dev.rand.agency/">сайте</a> """)

    #                          reply_markup=founder_keyboard_fc)
