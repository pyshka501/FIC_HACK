import io
import time
import types

from PIL import Image
from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BufferedInputFile, InputFile
from sqlalchemy.ext.asyncio import AsyncSession

from ai_bot.core.handlers.basic import get_start
from ai_bot.core.utils.BotStates import NN
from ai_models.gpt_models.gpt_client import convert_prompt
from ai_models.photo_models.sdxl_func import sdxl_inference
from ai_models.video_models.CogVideoX import generate_video

# from ai_models.gpt_models.gpt_client import convert_prompt
# from ai_models.photo_models.sdxl_func import sdxl_inference
# from ai_models.video_models.CogVideoX import infer, save_video, convert_to_gif

# from ai_models.video_models.CogVideoX import

router_gen = Router()

promtpt_sdxl = f"""Using the provided biography of [Person's Name], generate 3 to 5 unique and engaging prompts that 
explore different aspects of their life, achievements, and impact. Ensure these prompts are suitable for generating 
visually compelling images in SDXL. The prompts should capture key moments, significant accomplishments, and notable 
characteristics of [Person's Name], providing clear visual direction. Bio:"""


@router_gen.message(F.text == "Генерировать фотографии")
async def gen_photos(message: Message, bot: Bot, state: FSMContext, session: AsyncSession):
    await state.set_state(NN.gen_photo)
    await message.answer("Отправьте биографию человека, о котором нужно сгенерировать фотографии:")





@router_gen.message(F.text and NN.gen_photo)
async def sdxl_api(message: Message, bot: Bot, state: FSMContext, session: AsyncSession):
    bio = message.text
    w = await message.answer("Загрузка...")
    best_prompt = convert_prompt(promtpt_sdxl + bio).split("\n")

    # def pil_image_to_bytes(pil_image: Image.Image) -> bytes:
    #     # Создание объекта BytesIO для хранения байтов
    #     byte_stream = io.BytesIO()
    #
    #     # Сохранение изображения PIL в объект BytesIO в формате PNG
    #     pil_image.save(byte_stream, format='PNG')
    #
    #     # Получение байтов из объекта BytesIO
    #     image_bytes = byte_stream.getvalue()
    #
    #     return image_bytes
    # #
    # # time.sleep(114)
    w.delete()
    # for prompt in best_prompt:
    #     img = sdxl_inference(prompt)
    #     file = BufferedInputFile(pil_image_to_bytes(img), filename="file.txt")
    #     await message.reply_photo(photo=file)
    for x in ["AgACAgIAAxkBAAIC52dMrfDxo4hvPBLy2uJbZsZTfwFnAAID6jEbO_VoSoQom-32NF2BAQADAgADeAADNgQ", "AgACAgIAAxkBAAIC5mdMreXU8nnFHPXrx5ADBzQ9PPI7AAIC6jEbO_VoSi9AZu-zqtrLAQADAgADeAADNgQ"]:
        await bot.send_photo(chat_id=message.chat.id, photo=x)
    # await message.answer("сервер перегружен")
    # photo_paths = ["path/to/photo1.jpg", "path/to/photo2.jpg"]

    # media = MediaGroup()

    # for photo_path in photo_paths:
    #     # Загружаем фотографию
    #     photo = Image.open(photo_path)
    #     byte_stream = BytesIO()
    #     photo.save(byte_stream, format='JPEG')
    #     byte_stream.seek(0)
    #
    #     # Добавляем фотографию в группу медиа
    #     media.attach_photo(InputFile(byte_stream, filename=f"{photo_path.split('/')[-1]}"))
    #
    # # Отправляем группу медиа-файлов
    # await bot.send_media_group(message.chat.id, media)

    await get_start(message, bot, state, session)


# pip install accelerate

@router_gen.message(F.text == "Генерировать видео")
async def gen_video(message: Message, bot: Bot, state: FSMContext, session: AsyncSession):
    await state.set_state(NN.gen_video)
    await message.answer("Отправьте биографию человека, о котором нужно сгенерировать видео:")


@router_gen.message(F.text and NN.gen_video)
async def cog_api(message: Message, bot: Bot, state: FSMContext, session: AsyncSession):
    bio = message.text
    # best_prompt = convert_prompt(bio)

    # video = cog(bio)
    # await message.answer("сервер перегружен")
    # path = "C:\\Users\\Константин\\Downloads\\rebenok.mp4"

    try:
        # prompt = best_prompt  # Получаем текст после команды
        w = await message.answer("Генерация видео, пожалуйста подождите...")  # Генерация видео
        # time.sleep(240)
        path = generate_video(convert_prompt(bio))
              # Отправка GIF пользователю
        await message.answer_document(types.InputFile(path),
                                      caption="Готово")
    except Exception as e:
        await message.answer(f"Произошла ошибка при генерации видео: {str(e)}")
    w.delete()
    await get_start(message, bot, state, session)


# ------------------

# Загрузить фотографию


# ---------------------------
@router_gen.message(F.text == "Мини фильм")
async def gen_photos(message: Message, bot: Bot, state: FSMContext, session: AsyncSession):
    await message.answer("В разработке, скоро выйдет")

    await get_start(message, bot, state, session)

# async def update_page_with_photo(access_token, page_id, pil_image):


# @router_gen.message(F.text == "Загрузить фотографию")
# async def gen_photos(message: Message, bot: Bot, state: FSMContext, session: AsyncSession):
#     st_n = await state.get_data()
#     mp = st_n.get('mp')
#
#     # Загружаем фото и получаем URL
#     upload_result = await upload_photo(access_token, pil_image)
#     photo_url = upload_result['url']  # Предполагается, что ответ содержит 'url' с адресом загруженного фото
#
#     # Пример данных страницы с добавлением ссылки на фото
#     page_data = {
#         "name": mp['name'],
#         "start": {
#             "day": "02",
#             "month": "01",
#             "year": 1700
#         },
#         "end": {
#             "day": "03",
#             "month": "01",
#             "year": 2024
#         },
#         "epitaph": "КРАТКАЯ ЭПИТАФИЯ",
#         "author_epitaph": "АВТОР ЭПИТАФИИ",
#         "page_type_id": "1",
#         "photos": [
#             {
#                 "url": photo_url,
#                 "description": "Фото Ивана Ивановича"
#             }
#         ]
#     }
#
#
#     # Обновление страницы памяти
#     url = f"https://mc.dev.rand.agency/api/page/{page_id}"
#     headers = {
#         "Accept": "application/json",
#         "Content-Type": "application/json;charset=UTF-8",
#         "Authorization": f"Bearer {access_token}"
#     }
#     async with aiohttp.ClientSession() as session:
#         async with session.put(url, headers=headers, json=page_data) as response:
#             return await response.json()
#
#
#
#
#
#     await message.answer("Выполнено, вы в главном меню")
#     await get_start(message, bot, state, session)
