import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '5434219816:AAFQHWifiFmQQu8_cZ9yIHVi14vFQvVLPT8'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

#
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    if message.text == '/start':
        await message.reply('Hi, i am Bot in aiogram! Write me)')
    elif message.text == '/help':
        await message.reply('Пиши "Привет" или "Что ты умеешь?"')

@dp.message_handler()
async def answer(message: types.Message):
    if message.text == "Привет":
        await message.reply('Hi')
    elif message.text == 'Что ты умеешь?':
        await message.reply('Пока что умею только повторять за тобой, но скоро я стану круче')
    else:
        await message.reply(message.text)




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)