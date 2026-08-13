import os
import asyncio
from threading import Thread
from flask import Flask
from pyrogram import Client, filters
from pyrogram.enums import ChatType

# Render Web Service
web_app = Flask('')

@web_app.route('/')
def home():
    return "Userbot Web Service is running!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
STRING_SESSION = os.environ.get("STRING_SESSION")
SOURCE_CHANNEL_INPUT = os.environ.get("SOURCE_CHANNEL", "").strip().lower()

app = Client("userbot_session", session_string=STRING_SESSION, api_id=API_ID, api_hash=API_HASH)

TARGET_CHANNEL_ID = None

@app.on_message()
async def auto_forward(client, message):
    global TARGET_CHANNEL_ID
    
    if not message.chat:
        return

    # Check if the message is from our source channel
    chat_username = f"@{message.chat.username}".lower() if message.chat.username else ""
    chat_id = str(message.chat.id)

    if chat_username == SOURCE_CHANNEL_INPUT or chat_id == SOURCE_CHANNEL_INPUT or message.chat.id == TARGET_CHANNEL_ID:
        print(f"\n[+] MAXXANSA HAARAAN ARGAMEERA! ID: {message.id} | Channel: {message.chat.title}")
        
        group_count = 0
        async for dialog in client.get_dialogs():
            if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                group_count += 1
                try:
                    await message.forward(dialog.chat.id)
                    print(f"--> [SUCCESS] Gara '{dialog.chat.title}' ergameera.")
                    await asyncio.sleep(60) # Delay spam ittisuuf
                except Exception as e:
                    print(f"--> [ERROR] Gara '{dialog.chat.title}' erguu hin danda'amne: {e}")
        
        if group_count == 0:
            print("--> [WARNING] Group-ni haaraa tokkollee account kee irratti hin argamne!")

async def main():
    global TARGET_CHANNEL_ID
    Thread(target=run_web, daemon=True).start()
    await app.start()
    
    # Resolve Target Channel ID on start
    try:
        chat = await app.get_chat(SOURCE_CHANNEL_INPUT)
        TARGET_CHANNEL_ID = chat.id
        print(f"Userbot hojii eegaleera! Channel: '{chat.title}' (ID: {chat.id})")
    except Exception as e:
        print(f"Warning: Channel '{SOURCE_CHANNEL_INPUT}' resolve gochuun hin danda'amne: {e}")

    await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
