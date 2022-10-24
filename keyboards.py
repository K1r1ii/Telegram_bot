from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

#создание кнопок
kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = '/help'
kb.add(b1)

#создания inline клавиатуры(кнопки закреплены за крнкретным сообщением)
ikb = InlineKeyboardMarkup(row_width=2)
ib1 = InlineKeyboardButton(text='отзыв', url='https://t.me/Klr11111')
ikb.add(ib1)