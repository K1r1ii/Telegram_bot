from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

#создание кнопок
def get_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton('Заполнить анкету')
    b2 = KeyboardButton('Найти друга!')
    b3 = KeyboardButton('Посмотреть объявление')
    b4 = KeyboardButton('Мой баланс')
    kb.row(b1, b2)
    kb.row(b3, b4)
    return kb

#пользоватлеьская клавиатура, но для админа (+ переход обратно)
def get_keyboard_user_admin() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton('Заполнить анкету')
    b2 = KeyboardButton('Найти друга!')
    b3 = KeyboardButton('Посмотреть объявление')
    b4 = KeyboardButton('Мой баланс')
    b5 = KeyboardButton('Клавиатура админ')
    kb.row(b1, b2)
    kb.row(b3, b4)
    kb.row(b5)
    return kb

def get_admin_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    b1 = KeyboardButton('Создать объявление')
    b2 = KeyboardButton('Начислить баллы')
    b3 = KeyboardButton('Сменить пароль')
    b4 = KeyboardButton('Клавиатура пользователь')
    b5 = KeyboardButton('Получить базу данных')
    b6 = KeyboardButton('Создать напоминание')
    kb.row(b1, b2)
    kb.row(b3, b4)
    kb.row(b5, b6)
    return kb

#создания inline клавиатуры(кнопки закреплены за конкретным сообщением)
#inline кнопка для рекомендаций, содержит ссылку на рекомендуемого пользователя
def get_inline_keyboard_rec(url_tg) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=2)
    ib1 = InlineKeyboardButton(text='Начать общаться!', url=url_tg)
    ikb.add(ib1)
    return ikb

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