from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

#создание кнопок
def get_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton('Заполнить анкету')
    b2 = KeyboardButton('Найти друга!')
    b3 = KeyboardButton('Мой баланс')
    kb.add(b1).add(b2).add(b3)
    return kb

def get_admin_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton('Создать объявление')
    b2 = KeyboardButton('Начислить баллы')
    kb.add(b1).add(b2)
    return kb

#создания inline клавиатуры(кнопки закреплены за конкретным сообщением)
#inline кнопка для рекомендаций, содержит ссылку на рекомендуемого пользователя
def get_inline_keyboard_rec(url_tg) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=2)
    ib1 = InlineKeyboardButton(text='Начать общаться!', url=url_tg)
    ikb.add(ib1)
    return ikb

#inline кнопка для перехода к покупке товара
# def get_inline_keyboard_ads(admin_url) -> InlineKeyboardMarkup:
#     ikb = InlineKeyboardMarkup(row_width=2)
#     ib1 = InlineKeyboardButton(text='Купить!', url=admin_url)
#     ikb.add(ib1)
#     return ikb

def get_callback_keyboard() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=2)
    ib1 = InlineKeyboardButton(text='Купить!', callback_data='buy')
    ikb.add(ib1)
    return ikb

#inline кнопка для отзыва(ссылка на разработчика)
def get_inline_keyboard_feedback() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=2)
    ib1 = InlineKeyboardButton(text='отзыв', url='https://t.me/Klr11111')
    ikb.add(ib1)
    return ikb

#создания клавиатуры для сброса состояний(анкета)
def get_cancel_anketa() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Отменить заполнение анкеты'))
    return kb

#создание клавиатуры для сброса состояний(объявления)
def get_cancel_ads() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Отменить заполнение объявления'))
    return kb