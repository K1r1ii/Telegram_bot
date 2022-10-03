import logging
from aiogram import Bot, Dispatcher, executor, types
from function import Rock_Paper_Scissors

API_TOKEN = '5434219816:AAFQHWifiFmQQu8_cZ9yIHVi14vFQvVLPT8'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    if message.text == '/start':
        await message.reply('Hi, i am Bot in aiogram! Write me)')
    elif message.text == '/help':
        await message.reply('Hi, i can play "Rock, paper, scissors"\nWrite rock, paper or scissors and lets get started!')

@dp.message_handler()
async def game_bot(message: types.Message):
    move = message.text.lower()
    await message.answer(Rock_Paper_Scissors(move))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)