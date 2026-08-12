import os
import asyncio
from threading import Thread
from flask import Flask
from pyrogram import Client, filters
from pyrogram.enums import ChatType

# Web Server Render-iif barbaachisu (Akka inni active ta'uuf)
web_app = Flask('')

@web_app.route('/')
def home():
    return "Userbot is alive!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# Client setup
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
STRING_SESSION = os.environ.get("STRING_SESSION")
SOURCE_CHANNEL = os.environ.get("SOURCE_CHANNEL")

app = Client("userbot_session", session_string=STRING_SESSION, api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.chat(SOURCE_CHANNEL))
async def auto_forward(client, message):
    print(f"Maxxansi haaraan argameera ID: {message.id}")
    async for dialog in client.get_dialogs():
        if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            try:
                await message.forward(dialog.chat.id)
                print(f"Post-ni gara {dialog.chat.title} irratti ergameera.")
                await asyncio.sleep(15)
            except Exception as e:
                print(f"Gara {dialog.chat.title} erguun hin danda'amne: {e}")

if __name__ == "__main__":
    # Web server background irratti baneera
    Thread(target=run_web).start()
    print("Userbot hojii eegaleera...")
    app.run()
