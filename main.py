import os
import asyncio
from threading import Thread
from flask import Flask
from pyrogram import Client, filters
from pyrogram.enums import ChatType

# Render Web Service Keep-Alive
web_app = Flask('')

@web_app.route('/')
def home():
    return "Userbot Web Service is running!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# Environment Variables
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
STRING_SESSION = os.environ.get("STRING_SESSION")
SOURCE_CHANNEL = os.environ.get("SOURCE_CHANNEL")

app = Client("userbot_session", session_string=STRING_SESSION, api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.chat(SOURCE_CHANNEL))
async def auto_forward(client, message):
    print(f"\n[+] Maxxansi haaraan channel '{SOURCE_CHANNEL}' irraa argameera! Message ID: {message.id}")
    
    async for dialog in client.get_dialogs():
        if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            try:
                await message.forward(dialog.chat.id)
                print(f"--> [SUCCESS] Gara Group '{dialog.chat.title}' irratti ergameera.")
                # Delay amansiisaa (sekondii 60)
                await asyncio.sleep(60)
            except Exception as e:
                print(f"--> [ERROR] Gara Group '{dialog.chat.title}' erguun hin danda'amne: {e}")

async def main():
    Thread(target=run_web, daemon=True).start()
    print(f"Userbot hojii eegaleera! Channel hordofamu: {SOURCE_CHANNEL}")
    await app.start()
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
