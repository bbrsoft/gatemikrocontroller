from telethon import TelegramClient, events
import re
import subprocess
import json

# API credentials Telegram
api_id = 21508130  
api_hash = 'df34c286ae21ae3111c073fab928167c'
phone = '+6281127000212'

# Username bot target
bot_username = '@B16AIG_bot'

client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage(chats=bot_username))
async def new_message_handler(event):
    text = event.message.text
    print(f"📩 Pesan baru dari bot: {text}")

    # Jika mendeteksi pesan notif gerakan
    if "🚨 Gerakan terdeteksi!" in text:
        print("🚨 Menjalankan YOLO selama 5 detik...")
        process = subprocess.Popen(["python", "yolo_raspi_imou.py"])
        time.sleep(5)
        process.terminate()  # atau process.kill() jika terminate tidak cukup
        print("🛑 YOLO dihentikan.")

client.start()
client.run_until_disconnected()
