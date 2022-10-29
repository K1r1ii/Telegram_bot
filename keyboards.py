from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

#создание кнопок
def get_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton('Заполнить анкету')
    b2 = KeyboardButton('Найти друга!')
    b3 = KeyboardButton('Мой баланс')
    kb.add(b1).add(b2).add(b3)
    return kb

#создания inline клавиатуры(кнопки закреплены за конкретным сообщением)
#inline кнопка для рекомендаций, содержит ссылку на рекомендуемого пользователя
def get_inline_keyboard_rec(url_tg) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=2)
    ib1 = InlineKeyboardButton(text='Начать общаться!', url=url_tg)
    ikb.add(ib1)
    return ikb

#inline кнопка для отзыва(ссылка на разработчика)
def get_inline_keyboard_feedback() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=2)
    ib1 = InlineKeyboardButton(text='отзыв', url='https://t.me/Klr11111')
    ikb.add(ib1)
    return ikb

#создания клавиатуры для сброса состояний
def get_cancel() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Отменить заполнение'))
    return kb
