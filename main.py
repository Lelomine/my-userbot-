import os
import asyncio
from flask import Flask
from pyrogram import Client, filters
from pyrogram.enums import ChatType

# Render Web Service
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Userbot Web Service is active!"

# Environment variables
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
STRING_SESSION = os.environ.get("STRING_SESSION", "")
SOURCE_INPUT = os.environ.get("SOURCE_CHANNEL", "@Lalosport").strip()

app = Client("userbot_session", session_string=STRING_SESSION, api_id=API_ID, api_hash=API_HASH)

SOURCE_CHAT_ID = None

@app.on_message()
async def auto_forward(client, message):
    global SOURCE_CHAT_ID
    if not message.chat:
        return

    # Channel username fi ID unified check gochuuf:
    msg_uname = f"@{message.chat.username}".lower() if message.chat.username else ""
    msg_id = message.chat.id

    is_source = False
    if SOURCE_CHAT_ID and msg_id == SOURCE_CHAT_ID:
        is_source = True
    elif msg_uname == SOURCE_INPUT.lower():
        is_source = True

    if is_source:
        print(f"\n[+] MAXXANSA HAARAAN ARGAMEERA! ID: {message.id} | Channel: {message.chat.title}")
        
        async for dialog in client.get_dialogs():
            if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                try:
                    await message.forward(dialog.chat.id)
                    print(f"--> [SUCCESS] Gara Group '{dialog.chat.title}' ergameera.")
                    await asyncio.sleep(60)  # Delay amansiisaa (sekondii 60)
                except Exception as e:
                    print(f"--> [ERROR] Group '{dialog.chat.title}' irratti erguun dide: {e}")

async def start_services():
    global SOURCE_CHAT_ID
    import hypercorn.asyncio
    from hypercorn.config import Config

    config = Config()
    config.bind = [f"0.0.0.0:{os.environ.get('PORT', 8080)}"]
    
    await app.start()
    
    # Resolving channel chat ID
    try:
        chat = await app.get_chat(SOURCE_INPUT)
        SOURCE_CHAT_ID = chat.id
        print(f"\n==========================================")
        print(f"Userbot hojii eegaleera!")
        print(f"Target Channel: '{chat.title}' (ID: {chat.id})")
        print(f"==========================================\n")
    except Exception as e:
        print(f"\n[WARNING] Channel '{SOURCE_INPUT}' ID argachuun hin danda'amne: {e}\n")

    await hypercorn.asyncio.serve(web_app, config)

if __name__ == "__main__":
    asyncio.run(start_services())
