from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def chat_type(msg: types.Message):
    if msg.chat.type != "private":
        return False
    else:
        return True

def was_admin(callback: types.CallbackQuery):
    return callback.message.answer("Вышло обновление бота, нажмите - /start")