from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from function import Rock_Paper_Scissors
from config import *

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

#создание кнопок
kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = '/help'
kb.add(b1)

#создания inline клавиатуры(кнопки закреплены за крнкретным сообщением)
ikb = InlineKeyboardMarkup(row_width=2)
ib1 = InlineKeyboardButton(text='отзыв', url='https://t.me/Klr11111')
ikb.add(ib1)

#действия при команде старт
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(text = "Привет, я бот из команды /start!", reply_markup=kb)
    await message.delete()

#вызов функционала бота
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply(HELP_LIST, parse_mode='HTML')

#вызов описания бота
@dp.message_handler(commands=['description'])
async def description_command(message: types.Message):
    await message.answer(DESCRIPTION)
    await message.delete()

#функция по отправке стикера
@dp.message_handler(commands=['give'])
async def sticker(message: types.Message):
    await message.answer(text='Смотри какой крутой стикер!😁')
    await bot.send_sticker(message.from_user.id, sticker='CAACAgIAAxkBAAEGKlVjU7QwGyBjHsfhhVkRvLbk8gABwZkAAgwbAAIwRAlJ_5XxW1F1mngqBA')
    await message.delete()

#ответ стикером на стикер
@dp.message_handler(content_types=['sticker'])
async def send_sticker(message: types.Message):
    await bot.send_sticker(message.from_user.id, sticker='CAACAgIAAxkBAAEGKlVjU7QwGyBjHsfhhVkRvLbk8gABwZkAAgwbAAIwRAlJ_5XxW1F1mngqBA')

#тест inline клавиатуры, ссылка на профиль в телеграм
@dp.message_handler(commands=['feedback'])
async def send_feedback(message: types.Message):
    await message.answer(text='Если ты хочешь как то улучшить бота, то напиши нам отзыв!', reply_markup=ikb)

#развлекательная часть
@dp.message_handler()
async def game(message: types.Message):
    if message.text == '❤️':
        await message.answer('🖤')
    else:
        move = message.text
        await message.answer(text=Rock_Paper_Scissors(move))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)