import io

from PIL import Image
from aiogram import Bot, Router, F
from aiogram.client.session import aiohttp
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BufferedInputFile
from sqlalchemy.ext.asyncio import AsyncSession

from ai_bot.core.api_tools.request_api import get_individual_pages
from ai_bot.core.database.orm_query import get_access_token_db
from ai_bot.core.handlers.basic import get_start
from ai_bot.core.keyboards.keyboards import gen_menu
from ai_bot.core.utils.BotStates import Work, MemoryPage, NN
from colorization.colorizers.util import load_img
from colorization.demo_release import colorizier

router_mp = Router()


# @router_mp.message(F.text == "Найти страницу памяти" and Work.main_menu)
# async def find_mp(message: Message, bot: Bot, state: FSMContext, session: AsyncSession):

def format_page(i, page):
    return f"""
Страница памяти {i + 1}\n
Имя: {page['name'] or 'пусто'}
Фамилия: {page['surname'] or 'пусто'}
Отчество: {page['patronym'] or 'пусто'}\n
Дата рождения: {page['birthday_at'] or 'пусто'}
Дата смерти: {page['died_at'] or 'пусто'}\n
Эпитафия: {page['epitaph'] or 'пусто'}
Автор эпитафии: {page['author_epitaph'] or 'пусто'}\n
<a href="{page['link']}">Перейти к странице</a>
"""


def extract_photo_url(page):
    if page["main_image"]:
        return page["main_image"]
    elif page["media"]:
        # Предположим, что URL фотографии хранится в поле `file_name` в массиве `media`
        return [media_item["file_name"] for media_item in page["media"]]
    else:
        return None


@router_mp.message(F.text == "Просмотр всех страниц памяти")
async def get_all_mp(message: Message, bot: Bot, state: FSMContext, session: AsyncSession):
    wait = await message.answer('загрузка...')
    user_id = int(message.from_user.id)
    access_token = (await get_access_token_db(session, {"user_id": user_id}))[0].access_token
    print(access_token)

    individual_pages = [x for x in await get_individual_pages(access_token)]
    await wait.delete()

    #  pagination
    await state.update_data(individual_pages=individual_pages)
    # reply_markup=create_pagination_keyboard(page, total_pages))
    for i, x in enumerate(individual_pages):
        photo = extract_photo_url(x)
        if photo:
            await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=format_page(i, x))
        else:
            await message.answer(format_page(i, x))
    if len(individual_pages) != 0:
        await state.set_state(MemoryPage.all_memory)
        await message.answer("Напишите номер станицы, которую хотите выбрать")
    else:
        await message.answer("У вас нет страниц памяти. Вернитесь в главное меню")
        await get_start(message, bot, state, session)


@router_mp.message(F.text.isdigit() and MemoryPage.all_memory)
async def mp_menu(message: Message, bot: Bot, state: FSMContext, session: AsyncSession):
    if not F.text.isdigit():
        message.answer("Это не число, попробуйте еще раз:")

    n = int(message.text) - 1
    st_n = await state.get_data()
    individual_pages = st_n.get('individual_pages')

    photo = extract_photo_url(individual_pages[n])
    await state.set_state(MemoryPage.mp_menu)
    await state.update_data(mp=individual_pages[n])
    if photo:
        await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=format_page(n, individual_pages[n]),
                             reply_markup=gen_menu)
    else:
        await message.answer(format_page(n, individual_pages[n]), reply_markup=gen_menu)


# паигнация


# ---------------

async def get_image_pil(bot, file_id):
    file = await bot.get_file(file_id)
    file_path = file.file_path
    url = f'https://api.telegram.org/file/bot7704895926:AAFNv83AEux3MMLmT-DN7Z5nR6AufFEn18E/{file_path}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                image_data = await response.read()
                image = Image.open(io.BytesIO(image_data))
                return image
            else:
                raise Exception("Не удалось загрузить изображение")


@router_mp.message(F.text == "Разукрасить фотографию")
async def gen_photos(message: Message, bot: Bot, state: FSMContext, session: AsyncSession):
    await state.set_state(NN.colorize)
    await message.answer("Отправьте фотографию, которую необходимо разукрасить:")


@router_mp.message(F.photo)
async def handle_photo(message: Message, bot: Bot, state: FSMContext, session: AsyncSession):
    photo = message.photo[-1]  # Получаем фотографию самого высокого качества
    pil_image = load_img(await get_image_pil(bot, photo.file_id))

    image = colorizier(pil_image)

    def pil_image_to_bytes(pil_image: Image.Image) -> bytes:
        # Создание объекта BytesIO для хранения байтов
        byte_stream = io.BytesIO()

        # Сохранение изображения PIL в объект BytesIO в формате PNG
        pil_image.save(byte_stream, format='PNG')

        # Получение байтов из объекта BytesIO
        image_bytes = byte_stream.getvalue()

        return image_bytes

    file = BufferedInputFile(pil_image_to_bytes(image), filename="file.txt")
    await message.reply_photo(photo=file)
    await get_start(message, bot, state, session)


# =======
#
# =============

# from PIL import Image/


# Пример использовани

@router_mp.message(F.text == "Добавить страницу памяти" and Work.main_menu)
async def add_mp(message: Message, bot: Bot, state: FSMContext, session: AsyncSession):
    pass
