import os
import asyncio
from flask import Flask
from pyrogram import Client, filters
from pyrogram.enums import ChatType

# Render Web Service
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Userbot is running!"

# Variables
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
STRING_SESSION = os.environ.get("STRING_SESSION")
SOURCE_CHANNEL = os.environ.get("SOURCE_CHANNEL", "").strip()

app = Client("userbot_session", session_string=STRING_SESSION, api_id=API_ID, api_hash=API_HASH)

@app.on_message()
async def auto_forward(client, message):
    if not message.chat:
        return

    # Channel username ykn ID mirkaneessuu
    chat_uname = f"@{message.chat.username}" if message.chat.username else ""
    chat_id = str(message.chat.id)

    if chat_uname.lower() == SOURCE_CHANNEL.lower() or chat_id == SOURCE_CHANNEL:
        print(f"\n[+] MAXXANSA HAARAAN ARGAMEERA! ID: {message.id} | Channel: {message.chat.title}")
        
        async for dialog in client.get_dialogs():
            if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                try:
                    await message.forward(dialog.chat.id)
                    print(f"--> [SUCCESS] Gara Group '{dialog.chat.title}' ergameera.")
                    await asyncio.sleep(60) # Sekondii 60 delay
                except Exception as e:
                    print(f"--> [ERROR] Gara '{dialog.chat.title}' erguu hin danda'amne: {e}")

async def start_services():
    import hypercorn.asyncio
    from hypercorn.config import Config

    config = Config()
    config.bind = [f"0.0.0.0:{os.environ.get('PORT', 8080)}"]
    
    # Start Pyrogram Client
    await app.start()
    print(f"\n==========================================")
    print(f"Userbot hojii eegaleera! Channel: '{SOURCE_CHANNEL}'")
    print(f"==========================================\n")

    # Start Flask/Hypercorn Server
    await hypercorn.asyncio.serve(web_app, config)

if __name__ == "__main__":
    asyncio.run(start_services())
