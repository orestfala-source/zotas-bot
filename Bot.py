import asyncio
import random
import string
import os
from flask import Flask
import threading

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from supabase import create_client, Client

# --- Налаштування (замініть на власні дані) ---
TELEGRAM_BOT_TOKEN = "ВАШ_ТОКЕН_БОТА"
SUPABASE_URL = "https://ваш-проект.supabase.co"
SUPABASE_KEY = "ВАШ_ANON_KEY"
BANNER_URL = "https://i.imgur.com/your_banner_image.png"  # Посилання на банер бота

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 🌐 Веб-сервер Flask для підтримки 24/7 онлайну ---
app = Flask('')

@app.route('/')
def home():
    return "Zotas Visual Bot is active 24/7!"

def run_web_server():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

def keep_alive():
    t = threading.Thread(target=run_web_server)
    t.start()

# --- 🔑 Генерація ключа ---
def generate_key():
    part1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    part2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"ZOTAS-{part1}-{part2}"

# --- 🎹 Клавіатура (Інтерфейс як на скріншоті) ---
def main_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Купити підписку", callback_data="buy")],
        [
            InlineKeyboardButton(text="👤 Профіль", callback_data="profile"),
            InlineKeyboardButton(text="💬 Підтримка", url="https://t.me/ваш_нік_підтримки")
        ],
        [
            InlineKeyboardButton(text="📌 Мої ключі", callback_data="my_keys"),
            InlineKeyboardButton(text="📜 Документи / Інструкція", callback_data="docs")
        ]
    ])
    return keyboard

# --- 📩 Обробники команд та кнопок ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    caption_text = (
        "💡 **Привіт! Ласкаво просимо в Zotas Visual.**\n\n"
        "Оплачуючи підписку, ти отримуєш доступ до найкращих візуалів для Minecraft 1.21.4 Fabric."
    )
    
    # Надсилання картинки-банера з кнопками
    await message.answer_photo(
        photo=BANNER_URL,
        caption=caption_text,
        reply_markup=main_keyboard(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "buy")
async def process_buy(callback: types.CallbackQuery):
    telegram_id = callback.from_user.id
    new_key = generate_key()

    # Запис у Supabase
    supabase.table("licenses").insert({
        "key": new_key,
        "telegram_id": telegram_id,
        "active": 1
    }).execute()

    await callback.message.answer(
        f"✅ **Дякуємо за покупку!**\n\n"
        f"🔑 Твій ліцензійний ключ:\n`{new_key}`\n\n"
        f"Скопіюй його та введи при вході в майнкрафт.",
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data == "profile")
async def process_profile(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    res = supabase.table("licenses").select("*").eq("telegram_id", user_id).execute()
    keys_count = len(res.data)

    await callback.message.answer(
        f"👤 **Твій профіль:**\n\n"
        f"🆔 Telegram ID: `{user_id}`\n"
        f"🔑 Куплено ключів: {keys_count}",
        parse_mode="Markdown"
    )
    await callback.answer()

# --- 🚀 Запуск ---
async def main():
    keep_alive()  # Запускаємо фоновий веб-сервер
    print("Бот запущений!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())