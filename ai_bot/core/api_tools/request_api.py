import aiohttp
import asyncio
from preprocess.image_tools import pil_to_base64

async def get_access_token(email, password, device="bot-v0.0.1"):
    url = "https://mc.dev.rand.agency/api/v1/get-access-token"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json;charset=UTF-8"
    }
    data = {
        "email": email,
        "password": password,
        "device": device
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            json_response = await response.json()
            return json_response.get("access_token")

# access_token = await get_access_token("team02@hackathon.ru", "wHe7fVE7", "bot-v0.0.1")
# print(access_token)

access_token = "5549|oNyxw9j37RDrBjyvcf32WTwo3GwPt6jrjLzzxZGV"

async def search_page(access_token, name, slug, birthday_at, died_at, slugs, published_page, is_trusted):
    url = "https://mc.dev.rand.agency/api/page/search"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": f"Bearer {access_token}"
    }
    data = {
        "name": name,
        "slug": slug,
        "birthday_at": birthday_at,
        "died_at": died_at,
        "slugs": slugs,
        "published_page": published_page,
        "page": {"isTrusted": is_trusted}
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            return await response.json()

# pages = await search_page(access_token, "", "83050987", "", "", ["23647620"], 1, True)
# print(pages)

async def propose_relation(access_token, parent_id, relation_slug, kinship):
    url = "https://mc.dev.rand.agency/api/page/relative"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": f"Bearer {access_token}"
    }
    data = {
        "parentId": parent_id,
        "relation": relation_slug,
        "kinship": kinship
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            return await response.json()

# result = await propose_relation(access_token, 148, "19673642", 5)
# print(result)

async def get_individual_pages(access_token):
    url = "https://mc.dev.rand.agency/api/cabinet/individual-pages"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": f"Bearer {access_token}"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.json()

# individual_pages = await get_individual_pages(access_token)
# print(individual_pages[0])

async def get_page(access_token, page_id):
    url = f"https://mc.dev.rand.agency/api/page/{page_id}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": f"Bearer {access_token}"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.json()

# page = await get_page(access_token, 9972)
# print(page)

async def update_page(access_token, page_id, page_data):
    url = f"https://mc.dev.rand.agency/api/page/{page_id}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": f"Bearer {access_token}"
    }
    async with aiohttp.ClientSession() as session:
        async with session.put(url, headers=headers, json=page_data) as response:
            return await response.json()

# page_data = {
#     # Вставьте данные страницы памяти здесь
# }
# updated_page = await update_page(access_token, "23647620", page_data)
# print(updated_page)

async def upload_photo(access_token, pil_image):
    url = "https://mc.dev.rand.agency/api/media/upload"
    headers = {
        "Accept": "*/*",
        "Authorization": f"Bearer {access_token}"
    }
    img_base64 = pil_to_base64(pil_image)
    files = {'file': img_base64}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=files) as response:
            return await response.json()

# upload_result = await upload_photo(access_token, "test.jpg")
# print(upload_result)

async def add_comment(access_token, comment_data):
    url = "https://mc.dev.rand.agency/api/comment"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": f"Bearer {access_token}"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=comment_data) as response:
            return await response.json()

# comment_data = {
#     "test"
# }
# comment_result = await add_comment(access_token, comment_data)
# print(comment_result)

# Пример использования
# asyncio.run(search_page(access_token, "", "83050987", "", "", ["23647620"], 1, True))
if __name__ == "__main__":
    import aiohttp
    from aiogram import Bot, Dispatcher, types
    from aiogram.utils import executor
    from aiogram.dispatcher.filters import Command
    import json

    API_TOKEN = 'YOUR_BOT_API_TOKEN'
    ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'  # Убедитесь, что у вас есть актуальный access token

    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot)


    async def update_page(access_token, page_id, page_data):
        url = f"https://mc.dev.rand.agency/api/page/{page_id}"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json;charset=UTF-8",
            "Authorization": f"Bearer {access_token}"
        }
        async with aiohttp.ClientSession() as session:
            async with session.put(url, headers=headers, json=page_data) as response:
                return await response.json()


    @dp.message_handler(Command("update_page"))
    async def handle_update_page(message: types.Message):
        try:
            # Пример данных для обновления страницы памяти
            page_id = ""  # Укажите идентификатор страницы
            page_data = {
                "name": "Иванов Иван Иванович",
                "start": {
                    "day": "02",
                    "month": "01",
                    "year": 1700
                },
                "end": {
                    "day": "03",
                    "month": "01",
                    "year": 2024
                },
                "epitaph": "КРАТКАЯ ЭПИТАФИЯ",
                "author_epitaph": "АВТОР ЭПИТАФИИ",
                "page_type_id": "1"
            }

            # Обновление страницы памяти
            updated_page = await update_page(ACCESS_TOKEN, page_id, page_data)

            # Отправка сообщения пользователю о результате
            # await message.answer(f"Страница памяти обновлена: {json.dumps(updated_page, indent=2, ensure_ascii=False)}")

        except Exception as e:
            # await message.answer(f"Произошла ошибка: {str(e)}")
            print(e)



# Пример использования:
# access_token = "ВАШ_ACCESS_TOKEN"
# page_id = "23647620"
# pil_image = Image.open("test.jpg")
# result = await update_page_with_photo(access_token, page_id, pil_image)
# print(result)

