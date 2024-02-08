from pyrogram import Client, filters
import logging
import json
import os
from config import api_id, api_hash

logging.basicConfig(level=logging.INFO)

try:
    app = Client("my_account", api_id=api_id, api_hash=api_hash)
except Exception as e:
    print(f"Произошла ошибка при запуске приложения: {e}")
    input("Нажмите любую клавишу для выхода...")

with open('chat.json', 'r+') as file:
    file_data = json.load(file)
    if len(file_data) == 0:
        print('Вы не указали канал\nИспользуйте addchannel.bat чтобы добавить канал')
    else:
        @app.on_message(filters.channel)
        async def handle_message(client, message):
            for i in range(len(file_data)):
                if int(file_data[i]["chat_id"]) == int(message.chat.id):
                    if message.photo is not None and message.edit_date is None:
                        await process_photo_message(message, file_data[i]["tochannel"])
                    elif message.video is not None and message.edit_date is None:
                        await process_video_message(message, file_data[i]["tochannel"])
                    elif message.document is not None and message.edit_date is None:
                        await process_document_message(message, file_data[i]["tochannel"])
                    elif message.sticker is not None:
                        await process_sticker_message(message, file_data[i]["tochannel"])
                    elif message.voice is not None and message.edit_date is None:
                        await process_voice_message(message, file_data[i]["tochannel"])
                    elif message.poll is not None:
                        await process_poll_message(message, file_data[i]["tochannel"])
                    elif message.video_note is not None or message.animation is not None:
                        pass
                    elif message.edit_date is not None:
                        await process_edited_message(message, file_data[i]["tochannel"])
                    else:
                        await process_text_message(message, file_data[i]["tochannel"])

        async def process_photo_message(message, channels):
            d = await message.download()
            caption = f'\n{message.caption}' if message.caption else ''
            for c in channels:
                await app.send_photo(c, d, caption=caption)
            os.remove(d)

        async def process_video_message(message, channels):
            d = await message.download()
            caption = f'\n{message.caption}' if message.caption else ''
            for c in channels:
                await app.send_video(c, d, caption=caption)
            os.remove(d)

        async def process_document_message(message, channels):
            d = await message.download()
            caption = f'\n{message.caption}' if message.caption else ''
            for c in channels:
                await app.send_document(c, document=d, caption=caption)
            os.remove(d)

        async def process_sticker_message(message, channels):
            for c in channels:
                await app.send_sticker(c, message.sticker.file_id)

        async def process_voice_message(message, channels):
            d = await message.download()
            for c in channels:
                await app.send_voice(c, d)
            os.remove(d)

        async def process_poll_message(message, channels):
            options = [option.text for option in message.poll.options]
            question = message.poll.question
            poll = await app.send_poll(channels[0], question, options)
            for j in range(1, len(channels)):
                await app.forward_messages(channels[j], poll.chat.id, poll.message_id)

        async def process_edited_message(message, channels):
            for c in channels:
                await app.edit_message_text(c, message.text, message_id=message.message_id)

        async def process_text_message(message, channels):
            for c in channels:
                await app.send_message(c, f'\n{message.text}')

try:
    app.run()
except Exception as e:
    print(f"Произошла ошибка при запуске приложения: {e}")
    input("Нажмите любую клавишу для выхода...")
