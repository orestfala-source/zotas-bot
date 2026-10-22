import os
import hashlib
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from supabase import create_client, Client

# Отримуємо змінні середовища (або можете вписати напряму для тесту)
BOT_TOKEN = os.getenv("8928232684:AAGKMPYyPDjrGoC-1jbYl0wZzLblujl27yA")
SUPABASE_URL = os.getenv("https://gczypvqctklayezlvdss.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdjenlwdnFjdGtsYXllemx2ZHNzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTI2ODk5NzcsImV4cCI6MjEwODI2NTk3N30.ugrkQdj-trkn0a_WNbK78Z8DRLNuvgYDBLwnuW4KkJE")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Підключення до Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Головне меню з кнопкою купівлі
def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 Купити підписку Zontas Visuals", callback_data="buy_menu")]
    ])
    return keyboard

# Меню вибору тарифів (кількість днів та ціни)
def get_tariffs_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⏳ 30 днів — 200 грн (~$2)", url="ПОСИЛАННЯ_НА_ОПЛАТУ_ТУТ")],
        [InlineKeyboardButton(text="⏳ 60 днів — $2.50", url="ПОСИЛАННЯ_НА_ОПЛАТУ_ТУТ")],
        [InlineKeyboardButton(text="⏳ 90 днів — $3", url="ПОСИЛАННЯ_НА_ОПЛАТУ_ТУТ")],
        [InlineKeyboardButton(text="⏳ 180 днів — $7", url="ПОСИЛАННЯ_НА_ОПЛАТУ_ТУТ")],
        [InlineKeyboardButton(text="♾ Назавжди — $11", url="ПОСИЛАННЯ_НА_ОПЛАТУ_ТУТ")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")]
    ])
    return keyboard

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Вітаємо у **Zontas Visuals**!\n\n"
        "Це офіційний бот для купівлі та керування вашою ліцензією для моду.\n"
        "Натисніть кнопку нижче, щоб обрати підписку:",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "buy_menu")
async def show_tariffs(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🛒 **Оберіть термін підписки для Zontas Visuals:**\n\n"
        "Оберіть потрібний варіант нижче, щоб перейти до оплати:",
        reply_markup=get_tariffs_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "👋 Вітаємо у **Zontas Visuals**!\n\n"
        "Це офіційний бот для купівлі та керування вашою ліцензією для моду.\n"
        "Натисніть кнопку нижче, щоб обрати підписку:",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

if __name__ == "__main__":
    import asyncio
    print("Бот запущено успішно!")
    asyncio.run(dp.start_polling(bot))
