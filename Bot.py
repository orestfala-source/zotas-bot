import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from supabase import create_client, Client

# Вставьте ваш реальный токен от BotFather в кавычки ниже:
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8928232684:AAGKMPYyPDjrGoC-1jbYl0wZzLblujl27yA")
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://gczypvqctklayezlvdss.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdjenlwdnFjdGtsYXllemx2ZHNzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTI2ODk5NzcsImV4cCI6MjEwODI2NTk3N30.ugrkQdj-trkn0a_WNbK78Z8DRLNuvgYDBLwnuW4KkJE")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Подключение к Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Главное меню с кнопкой покупки
def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 Купить подписку Zontas Visuals", callback_data="buy_menu")]
    ])
    return keyboard

# Меню выбора тарифов (сроки и цены)
def get_tariffs_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⏳ 30 дней — 200 грн (~$2)", url="ПОСИЛАННЯ_НА_ОПЛАТУ_ТУТ")],
        [InlineKeyboardButton(text="⏳ 60 дней — $2.50", url="ПОСИЛАННЯ_НА_ОПЛАТУ_ТУТ")],
        [InlineKeyboardButton(text="⏳ 90 дней — $3", url="ПОСИЛАННЯ_НА_ОПЛАТУ_ТУТ")],
        [InlineKeyboardButton(text="⏳ 180 дней — $7", url="ПОСИЛАННЯ_НА_ОПЛАТУ_ТУТ")],
        [InlineKeyboardButton(text="♾ Навсегда — $11", url="ПОСИЛАННЯ_НА_ОПЛАТУ_ТУТ")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")]
    ])
    return keyboard

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Добро пожаловать в **Zontas Visuals**!\n\n"
        "Это официальный бот для покупки и управления вашей лицензией для мода.\n"
        "Нажмите кнопку ниже, чтобы выбрать подписку:",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "buy_menu")
async def show_tariffs(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🛒 **Выберите срок подписки для Zontas Visuals:**\n\n"
        "Выберите нужный вариант ниже, чтобы перейти к оплате:",
        reply_markup=get_tariffs_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "👋 Добро пожаловать в **Zontas Visuals**!\n\n"
        "Это официальный бот для покупки и управления вашей лицензией для мода.\n"
        "Нажмите кнопку ниже, чтобы выбрать подписку:",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

if __name__ == "__main__":
    import asyncio
    print("Бот успешно запущен!")
    asyncio.run(dp.start_polling(bot))
