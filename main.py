import os
import re
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

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# Environment Variables
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
STRING_SESSION = os.environ.get("STRING_SESSION", "")
SOURCE_INPUT = os.environ.get("SOURCE_CHANNEL", "@Lalosport").strip()

app = Client("userbot_session", session_string=STRING_SESSION, api_id=API_ID, api_hash=API_HASH)

# Web server thread addaatiin jalqabsiisuu
Thread(target=run_web, daemon=True).start()

def clean_text(text: str) -> str:
    """Text keessaa linkii fi username kana haqa"""
    if not text:
        return ""
    
    # Linkiiwwan HTTP/HTTPS haquu
    text = re.sub(r'https?://\S+', '', text)
    # Linkiiwwan t.me haquu
    text = re.sub(r't\.me/\S+', '', text)
    # Usernames (@channel_name) haquu
    text = re.sub(r'@\w+', '', text)
    
    # Sarara duwwaa fi space dharraa qulqulleessuu
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)

@app.on_message()
async def auto_forward(client, message):
    if not message.chat:
        return

    msg_uname = f"@{message.chat.username}".lower() if message.chat.username else ""
    msg_id = str(message.chat.id)
    target_clean = SOURCE_INPUT.lower()

    # Channel match gochuu
    if msg_uname == target_clean or msg_id == target_clean or target_clean in msg_uname:
        print(f"\n[+] MAXXANSA HAARAAN ARGAMEERA! ID: {message.id} | Channel: {message.chat.title}")
        
        # Post text/caption qulqulleessuu
        raw_text = message.text or message.caption or ""
        cleaned_text = clean_text(raw_text)
        
        async for dialog in client.get_dialogs():
            if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                try:
                    # Yoo post-ni Suuraa/Video qabaate
                    if message.photo or message.video or message.document:
                        await message.copy(
                            chat_id=dialog.chat.id,
                            caption=cleaned_text
                        )
                    # Yoo Barreeffama qofa ta'e
                    elif cleaned_text:
                        await client.send_message(
                            chat_id=dialog.chat.id,
                            text=cleaned_text
                        )
                    
                    print(f"--> [SUCCESS] Post-ni qulqulla'aa ta'ee gara Group '{dialog.chat.title}' ergameera.")
                    await asyncio.sleep(180)  # Delay amansiisaa (sekondii 180 / minitii 3)
                except Exception as e:
                    print(f"--> [ERROR] Group '{dialog.chat.title}' irratti erguun dide: {e}")

print(f"\n==========================================")
print(f"Userbot (Link Cleaner) hojii eegaluuf qophaa'aa jira... Target: '{SOURCE_INPUT}'")
print(f"==========================================\n")

if __name__ == "__main__":
    app.run()
