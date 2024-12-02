from ai_bot.core.keyboards.reply import get_reply_keyboard


main_menu = get_reply_keyboard(
            "Просмотр всех страниц памяти",
            "Разукрасить фотографию",
            placeholder="Что вас интересует?",
            sizes=(1,1)
        )

mp_menu = get_reply_keyboard(
            "Сгенерировать контент",
            "Изменить данные",
            "Загрузить фотографию",
            "Связать страницы памяти",
            placeholder="Что вас интересует?",
            sizes=(2,2)
        )

gen_menu = get_reply_keyboard(
            "Генерировать фотографии",
            "Генерировать видео",
            "Загрузить фотографию",
            placeholder="Что вас интересует?",
            sizes=(2,1)
)
