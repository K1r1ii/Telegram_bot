import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '5434219816:AAFQHWifiFmQQu8_cZ9yIHVi14vFQvVLPT8'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def send_welcome(message: types.Message):
    await message.reply(message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)