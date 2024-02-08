from pyrogram import Client, raw
import json

API_ID = 99999999
API_HASH = ''
CHAT_FILE = 'chat.json'

app = Client('my_account', api_id=API_ID, api_hash=API_HASH)
app.start()

async def main():
    text = input('Введите название канала, чтобы добавить (точь в точь): ')
    async for dialog in app.get_dialogs():
        if dialog.chat.title and text in dialog.chat.title:
            with open(CHAT_FILE, 'r+') as file:
                try:
                    file_data = json.load(file)
                except json.decoder.JSONDecodeError:
                    file_data = []
                if not any(text == item['name'] for item in file_data):
                    a = {"name": dialog.chat.title,
                         "chat_id": dialog.chat.id, "tochannel": []}
                    file_data.append(a)
                    file.seek(0)
                    json.dump(file_data, file, indent=4)
                    print(f'Канал <{dialog.chat.title}> успешно добавлен.')
                else:
                    print("Канал уже добавлен")

app.run(main())
