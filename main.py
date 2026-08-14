import os
import asyncio
from threading import Thread
from flask import Flask
from pyrogram import Client, filters
from pyrogram.enums import ChatType

# Render Web Service Keep-Alive
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Userbot Web Service is Active!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# Variables
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
                    await asyncio.sleep(60) # Delay sekondii 60
                except Exception as e:
                    print(f"--> [ERROR] Group '{dialog.chat.title}' irratti erguun dide: {e}")

async def main():
    global SOURCE_CHAT_ID
    
    # Web server thread addaatiin jalqabsiisuu
    Thread(target=run_flask, daemon=True).start()
    
    # Telegram Client start gochuu
    await app.start()
    
    try:
        chat = await app.get_chat(SOURCE_INPUT)
        SOURCE_CHAT_ID = chat.id
        print(f"\n==========================================")
        print(f"Userbot hojii eegaleera!")
        print(f"Target Channel: '{chat.title}' (ID: {chat.id})")
        print(f"==========================================\n")
    except Exception as e:
        print(f"\n[WARNING] Channel '{SOURCE_INPUT}' ID argachuun hin danda'amne: {e}\n")

    await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
