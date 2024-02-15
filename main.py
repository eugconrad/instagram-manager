import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

from telethon import TelegramClient, events
from telethon.tl.types import Message

from instagrapi import Client as InstagramClient

from moviepy.editor import VideoFileClip

load_dotenv()

IG_USERNAME = os.getenv('IM_IG_USERNAME')
IG_PASSWORD = os.getenv('IM_IG_PASSWORD')

CAPTION = "Прояви актив! Поставь свой царский лайк ❤️ и подпишись @vidos.mem4ik 🔥🤝\n" \
          "• ~~~~~ •\n" \
          "🔹 Всем хорошего и приятного дня! 👌\n" \
          "🔹 Спасибо за поддержку! 🤝\n" \
          "• ~~~~~ •\n" \
          "🔸 Подпишись на новые видосы ➡️ @vidos.mem4ik 🔔\n" \
          "🔸 Отмечай друзей 👫\n" \
          "🔸 Оставляй комментарии ⌨️\n" \
          "🔸 Новые посты каждый день 📆\n" \
          "• ~~~~~ •\n" \
          "#юмор #смех #приколы #прикол #смешно " \
          "#ржака #шутка #ржач #мемы #позитив #любовь " \
          "#смешноевидео #видео #угар #шутки #улыбка " \
          "#жизнь #мем #весело #камеди #humor #лол " \
          "#лайк"

API_ID = 2040
API_HASH = "b18441a1ff607e10a989891a5462e627"
DEVICE_MODEL = "PC 64bit"
SYSTEM_VERSION = "Windows 10"
APP_VERSION = "4.6"
LANG_CODE = "ru"
SYSTEM_LANG_CODE = "ru-RU"

CHATS = [-1001961838181, -1001123683328]


class InstagramManager:
    tg_client: TelegramClient
    ig_client: InstagramClient

    def __init__(self):
        self.tg_client = TelegramClient(
            session="ig_manager",
            api_id=API_ID,
            api_hash=API_HASH,
            device_model=DEVICE_MODEL,
            system_version=SYSTEM_VERSION,
            app_version=APP_VERSION,
            lang_code=LANG_CODE,
            system_lang_code=SYSTEM_LANG_CODE
        )
        self.ig_client = InstagramClient()

    async def init(self):
        await self.tg_client.start()
        self.ig_client.login(IG_USERNAME, IG_PASSWORD)
        # Добавляем обработчик сообщений
        self.tg_client.add_event_handler(self.on_message, events.NewMessage(incoming=True, outgoing=False, chats=CHATS))
        print("Started.")
        await self.tg_client.run_until_disconnected()

    async def on_message(self, event):
        # Если это не сообщение
        if not isinstance(event.message, Message):
            return
        # Получаем обьект сообщения
        message: Message = event.message
        # Получаем видео
        print(message.media)
        if message.media and message.media.document.mime_type == "video/mp4" \
                and message.message == "Видео Долбоёба. Подписаться":
            file_name = await self.tg_client.download_media(message)
            # Загрузка видео
            video = VideoFileClip(file_name)
            # Получение соотношения сторон
            width, height = video.size
            aspect_ratio = width / height
            print(aspect_ratio)
            # Определение, является ли соотношение сторон 9:16
            is_stories = abs(aspect_ratio - (9 / 16)) < 0.01
            if is_stories:
                print('Соотношение сторон подходит для сторис')
                self.ig_client.video_upload_to_story(
                    path=Path(file_name),
                    caption=CAPTION
                )
            else:
                print(f'Соотношение сторон не подходит для сторис')
                self.ig_client.video_upload(
                    path=Path(file_name),
                    caption=CAPTION
                )
            print('Видео успешно Загружено.')
            try:
                os.remove(file_name)
            except:
                pass
            try:
                os.remove(file_name + ".jpg")
            except:
                pass


async def main():
    instagram_manager = InstagramManager()
    await instagram_manager.init()


if __name__ == "__main__":
    asyncio.run(main())
