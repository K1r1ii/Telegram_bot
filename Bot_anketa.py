from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from keyboards import *
from config import *
from sqlite_bot.sqlite import *
from aiogram.types import InputFile

import datetime
import asyncio
from config import DESC_REMINDER

#запуск базы данных(создание)
async def on_startup(_):
    await db_start()

#создания экземпляра бота, диспетчера, и состояний
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot= bot, storage=storage)

#значения, которые будут задваться с аккаунта администратора
start_score = 10


#создание класса для состояний(анкета)
class Anketa_states_group(StatesGroup):
    photo = State()
    name = State()
    age = State()
    desc = State()
    url_tg = State()

#создание класса для состояний(объявления)
class Ads_states_group(StatesGroup):
    photo = State()
    desc = State()
    price = State()
    count_product = State()

#начисление баллов
class Earn_points(StatesGroup):
    name_user = State()
    count_points = State()

#создание пароля
class Entrance(StatesGroup):
    password = State()

#для смены пароля
class New_password(StatesGroup):
    old_pass = State()
    new_pass = State()

#удаление объявлений
class Delete_ads(StatesGroup):
    num_ads = State()

#создание напоминаний
class question(StatesGroup):
    q1 = State()
    q2 = State()

group_id = 0
count_desc = 0
count_remind = 0

#######################################   Обработчики вспомогательных команд   ####################################
#действия при команде старт
count_start = 0
admin_id = 0 #id администратора бота(HR)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message) -> None:
    global count_start
    await create_password()
    if message.from_user.id == admin_id:
        if count_start == 0:
            first_salary(user_id=message.from_user.id)
            count_start += 1
        await message.answer(text=START_ADMIN, reply_markup=get_admin_keyboard())
        await message.delete()
    else:
        if count_start == 0:
            first_salary(user_id=message.from_user.id)
            count_start += 1
        await message.answer(text=START, reply_markup=get_keyboard())
        await message.delete()
    await bot.send_sticker(message.chat.id,
                           sticker="CAACAgIAAxkBAAEGbuljc84s_rVQgwxv4EFXsNNHVkhV6QACpR0AArFpoEvs_tAZAQwhJysE")

@dp.message_handler(commands=['start_remind'])      #запоминаем id группы
async def host_f(message: types.Message):
    global group_id
    global count_remind
    if count_remind == 0:
        group_id = message.chat.id
        count_remind += 1

#отмена заполнения анкеты, сброс состояний
@dp.message_handler(Text(equals='Отменить заполнение анкеты', ignore_case=True), state='*')
async def cancel_command(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.answer(text='Заполнение анкеты отменено',
                         reply_markup=get_keyboard())
    await delete_profile(user_id=message.from_user.id)
    await state.finish()

#отмена заполнения объявления, сброс состояний
@dp.message_handler(Text(equals='Отменить заполнение объявления', ignore_case=True), state='*')
async def cancel_command(message: types.Message, state: FSMContext) -> None:
    if message.from_user.id == admin_id:
        current_state = await state.get_state()
        if current_state is None:
            return
        await message.answer(text='Заполнение объявления отменено',
                             reply_markup=get_admin_keyboard())
        c = delete_ads(num_current_ads())
        await state.finish()
    else:
        await message.answer(text='У вас недостаточно прав для этой операции(')

#функция удаления профиля
@dp.message_handler(commands=['deleteprofile'])
async def delete_command(message: types.Message):
    await delete_profile(user_id=message.from_user.id)
    await message.answer(text='Ваша анкета удалена',
                         reply_markup=get_keyboard())

#вызов функционала бота
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    if message.from_user.id == admin_id:
        await message.reply(HELP_ADMIN_LIST, parse_mode='HTML')
    else:
        await message.reply(HELP_LIST, parse_mode='HTML')

#вызов описания бота
@dp.message_handler(commands=['description'])
async def description_command(message: types.Message):
    await message.answer(DESCRIPTION)
    await message.delete()

#отзыв
@dp.message_handler(commands=['feedback'])
async def feedback_command(message: types.Message):
    await message.answer(text='хочешь оставить отзыв? пиши сюда!',
                         reply_markup=get_inline_keyboard_feedback())

#функция, вызывающая заданный админом вопрос от бота
@dp.message_handler(commands=['question'])
async def questions(message: types.Message):
    global count_zp, question_text
    await bot.send_message(chat_id=message.chat.id, text=question_text)
    count_zp = 0

#функция, возвращающая баланс текущего пользователя
@dp.message_handler(Text(equals='Мой баланс', ignore_case=True))
async def balans(message: types.Message):
    await bot.send_message(message.from_user.id, text=balans_inf(user_id=message.from_user.id))

#отправка все бд в текстовом формате админу
@dp.message_handler(Text(equals='Получить базу данных', ignore_case=True))
async def all_db_cmd(message: types.Message):
    if message.from_user.id == admin_id:
        with open('all_db.txt', 'w', encoding='utf-8') as f:
            db = all_db()
            db_list = []
            db_list_all = []
            for i in range(len(db)):
                for j in range(len(db[i])):
                    db_list.append(db[i][j])
                db_list_all.append(db_list)
                db_list = []
            for i in range(len(db_list_all)):
                for j in range(len(db_list_all[i])):
                    f.write(''.join(db_list_all[i][j]) + ' ')
                f.write('\n')
                f.write('\n')
        await message.answer_document(InputFile('all_db.txt'))
    else:
        await message.answer('У вас недостаточно прав для этой операции(')

#смена клавиатуры для админа
@dp.message_handler(Text(equals='клавиатура админ', ignore_case=True))
async def key(message: types.Message):
    if message.from_user.id == admin_id:
        await message.answer('Вы перешли на клавиатуру для администратора!',
                             reply_markup=get_admin_keyboard())
    else:
        await message.answer('У вас недостаточно прав для этой операции(')

@dp.message_handler(Text(equals='клавиатура пользователь', ignore_case=True))
async def key(message: types.Message):
    if message.from_user.id == admin_id:
        await message.answer('Вы перешли на клавиатуру для пользователя!',
                             reply_markup=get_keyboard_user_admin())
    else:
        await message.answer('У вас недостаточно прав для этой операции(')


#######################################   Рекомендации   ####################################
#функция, отвечающая за рекомендации другим пользователям
#счетчик count нужен для того, чтобы избежать отправки анкеты, которая уже была отправлена
count = 0
count_zp = 0
@dp.message_handler(Text(equals='Найти друга!', ignore_case=True))
async def rec_command(message: types.Message):
    global count
    if balans_inf(user_id=message.from_user.id)== -1:
        await message.answer('Для начала создайте анкету')
    else:
        now_balans = balans_inf(user_id=message.from_user.id)
        if now_balans >= start_score:
            if type(rec(user_id=message.from_user.id, count=count)) == str:     #если мы отправляем строку, значит дошли до конца в списке анкет, предупреждаем польхователя, обнуляем счетчик и начинаем сначала
                await message.answer(text=rec(user_id=message.from_user.id, count=count))
                count = 0
            else:   #если тип не строчный(список), то собираем и отправляем анкету, увеличивая счетчик
                waste(user_id=message.from_user.id)
                await bot.send_message(message.from_user.id, text='С вашего счета списано 10 валют!')
                m = rec(user_id=message.from_user.id, count=count)
                await bot.send_photo(message.from_user.id,
                                     photo=m[1],
                                     caption=f'{m[2]}, {m[3]}\n{m[4]}',
                                     reply_markup=get_inline_keyboard_rec(m[5]))
                count += 1
        else:
            await bot.send_message(message.from_user.id, text='На счету не хватает денег, видимо пора отвечать на вопросы в общем чате!')

#рекомендация объявлений
count_ads = 0 #кол-во просмотров объявлений
admin_url = 'https://t.me/Klr11111' #пока что моя ссылка, позже будет ссылка на акк админа(HR)
@dp.message_handler(Text(equals='посмотреть объявление', ignore_case=True))
async def rec_command_ads(message: types.Message):
    global count_ads
    if type(rec_ads(count_ads=count_ads)) == str:  # если мы отправляем строку, значит дошли до конца в списке объявлений, предупреждаем пользователя, обнуляем счетчик и начинаем сначала
        await message.answer(text=rec_ads(count_ads))
        count_ads = 0
    else:  # если тип не строчный(список), то собираем и отправляем объявление, увеличивая счетчик
        m = rec_ads(count_ads)
        await bot.send_photo(message.from_user.id,
                             photo=m[1],
                             caption=f'{m[2]}\nЦена: {m[3]}\nКоличество: {m[4]}',
                             reply_markup=get_callback_keyboard()
                             )
        count_ads += 1

#действие при нажатии callback кнопки
@dp.callback_query_handler(text='buy')
async def buy_ads(call: types.CallbackQuery):
    now_balans = balans_inf(user_id=call.from_user.id)
    if now_balans >= price(count_ads=count_ads - 1):
        if admin_id != 0:
            await call.message.answer('Покупка совершена!')
            change_data(count_ads=count_ads - 1, user_id=call.from_user.id)
            await call.message.answer(f'С вашего счета списано {price(count_ads=count_ads - 1)}')
            string = "<a href=" + f'"{tg_url(user_id=call.from_user.id)}"' + '>'+ f'{name(user_id=call.from_user.id)}' + '</a> купил этот товар!'
            await bot.send_message(admin_id, string, parse_mode='HTML')
            m = rec_ads(count_ads - 1)
            await bot.send_photo(admin_id,
                                 photo=m[1],
                                 caption=f'{m[2]}\nЦена: {m[3]}\nКоличество: {m[4]}'
                                 )
            await count_product(num(count_ads=count_ads-1))
        else:
            await call.message.answer('Администратор пока не авторизован, попробуйте позже')
    else:
        await call.message.answer('У вас недостаточно средств')

#######################################   Создание объявления   ####################################
#СДЕЛАТЬ НОВЫЙ КЛЮЧ ДЛЯ ТАБЛИЦЫ ОБЪЯВЛЕНИЙ (нужно избавиться от счетчиков в коде)

@dp.message_handler(Text(equals='Создать объявление', ignore_case=True), state=None)
async def start_ad(message: types.Message) -> None:
    if message.from_user.id == admin_id:
        await Ads_states_group.photo.set()
        await create_ads()
        await message.answer('Отправь фото товара(услуги)', reply_markup=get_cancel_ads())
    else:
        await message.answer('У вас недостаточно прав для этой операции(')

@dp.message_handler(lambda message: not message.photo, state=Anketa_states_group.photo)
async def check_photo_ads(message: types.Message):
    return await message.reply('Это не фото')

#сохраняем отправленное фото и справшиваем об имени(переходим к следующему состоянию)
@dp.message_handler(lambda message: message.photo, content_types=['photo'], state=Ads_states_group.photo)
async def load_photo_ads(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo_ads'] = message.photo[0].file_id
    await Ads_states_group.next()
    await message.answer('Опиши товар')

@dp.message_handler(state=Ads_states_group.desc)
async def load_name_ads(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc_ads'] = message.text
    await Ads_states_group.next()
    await message.answer('Какая будет цена?')

@dp.message_handler(state=Ads_states_group.price)
async def load_name_ads(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price_ads'] = message.text
    await Ads_states_group.next()
    await message.answer('Сколько будет товара?')

@dp.message_handler(state=Ads_states_group.count_product)
async def load_count_product_ads(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['count_product_ads'] = message.text
    await message.answer(text='Объявление готово',
                         reply_markup=get_admin_keyboard())
    await bot.send_photo(message.from_user.id,
                         photo=data['photo_ads'],
                         caption=f'{data["desc_ads"]}\nЦена: {data["price_ads"]}\nКоличество: {data["count_product_ads"]}'
                         )
    await edit_ads(state)
    await state.finish()

#######################################   Создание Анкеты   ####################################

#начинаем создавать анкету
@dp.message_handler(Text(equals='Заполнить анкету', ignore_case=True), state=None)
async def start_anketa(message: types.Message) -> None:
    await Anketa_states_group.photo.set()
    await create_profile(user_id=message.from_user.id)
    await message.answer('Отправь мне свое фото', reply_markup=get_cancel_anketa())

#проверяем корректность отправки фото
@dp.message_handler(lambda message: not message.photo, state=Anketa_states_group.photo)
async def check_photo(message: types.Message):
    return await message.reply('Это не фото')

#сохраняем отправленное фото и справшиваем об имени(переходим к следующему состоянию)
@dp.message_handler(lambda message: message.photo, content_types=['photo'], state=Anketa_states_group.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await Anketa_states_group.next()
    await message.answer('Как тебя зовут?')

#сохраняем имя и спрашиваем возраст(переход к следующему состоянию)
@dp.message_handler(state=Anketa_states_group.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await Anketa_states_group.next()
    await message.answer('Сколько тебе лет?')

#сохраняем возраст и спрашиваем описание, переходим к новому состоянию
@dp.message_handler(state=Anketa_states_group.age)
async def load_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text
    await Anketa_states_group.next()
    await message.answer('А теперь расскажи немного о себе(3-4 предложения)')

#сохраняем описание и выводим готовую анкету вида: фото + описание, очищаем состояния
@dp.message_handler(state=Anketa_states_group.desc)
async def load_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
    await  Anketa_states_group.next()
    await message.answer('Отправь мне ссылку на твой профиль в Телеграме')

@dp.message_handler(state=Anketa_states_group.url_tg)
async def load_url(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text[0] == '@':
            user_url = 'https://t.me/' + message.text[1:]
        else:
            user_url = message.text
        data['url_tg'] = user_url
    await message.answer(text='Анкета готова!',
                         reply_markup=get_keyboard())
    await bot.send_photo(message.from_user.id,
                         photo=data['photo'],
                         caption=f'{data["name"]}, {data["age"]}\n{data["desc"]}'
                         )
    await edit_profile(state, user_id=message.from_user.id, score=start_score)
    await state.finish()

#######################################   Вход в акк админа   ####################################

@dp.message_handler(Text(equals='Войти', ignore_case=True), state=None)
async def enter(message: types.Message) -> None:
    await Entrance.password.set()
    await message.answer('Введите пароль')

@dp.message_handler(state=Entrance.password)
async def check_password(message: types.Message, state: FSMContext):
    global admin_id

    if message.text == current_pass():
        admin_name = name(user_id=message.from_user.id)
        if admin_name == 'Вы не авторизованы, заполните анкету':
            await message.answer(admin_name)
        else:
            await message.answer(f'{admin_name}, вы вошли в аккаунт администратора, введите "/help", чтобы подробнее узнать о ваших возможностях',
                                 reply_markup=get_admin_keyboard())
            admin_id = message.from_user.id
    else:
        await message.answer('Введен неверный пароль')
    await state.finish()

#######################################   Смена пароля для аккаунта админа   ####################################

@dp.message_handler(Text(equals='Сменить пароль', ignore_case=True), state=None)
async def change_password_cmd(message: types.Message) -> None:
    if message.from_user.id == admin_id:
        await New_password.old_pass.set()
        await message.answer('Введите старый пароль')
    else:
        await message.answer('У вас недостаточно прав для этой операции(')

@dp.message_handler(state=New_password.old_pass)
async def check_old_pass(message: types.Message, state: FSMContext):
    if message.text == current_pass():
        await New_password.next()
        await message.answer('Введите новый пароль')
    else:
        await message.answer('Введен неверный пароль')
        await state.finish()

@dp.message_handler(state=New_password.new_pass)
async def new_pass_cmd(message: types.Message, state: FSMContext):
    await message.answer(text=str(change_password(message.text)))
    await state.finish()


#######################################   Начисление баллов   ####################################

@dp.message_handler(Text(equals='Начислить баллы', ignore_case=True), state=None)
async def points_for_user(message: types.Message) -> None:
    if message.from_user.id == admin_id:
        await Earn_points.name_user.set()
        await message.answer('Напиши имя того, кому хотел бы начислить баллы(имя указанное в его анкете)')
    else:
        await message.answer('У вас недостаточно прав для этой операции(')

@dp.message_handler(state=Earn_points.name_user)
async def load_name_user(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_user'] = message.text
    await Earn_points.next()
    await message.answer('Сколько баллов начислить?')

@dp.message_handler(state=Earn_points.count_points)
async def load_count_points(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['count_points'] = int(message.text)
    if type(find_user(data['name_user'])) == str:
        await message.answer(text=find_user(data['name_user']))
    else:
        salary(user_id=find_user(data['name_user']), summ=data['count_points'])
        await message.answer(text='баллы начислены!')
        await bot.send_message(find_user(data['name_user']), text=f'Вам начислено {data["count_points"]} баллов!')
    await state.finish()

#######################################   удаление объявления по его номеру   ####################################

@dp.message_handler(Text(equals='Удалить объявление', ignore_case=True), state=None)
async def del_ads_cmd(message: types.Message) -> None:
    if message.from_user.id == admin_id:
        await Delete_ads.num_ads.set()
        await message.answer('Напиши номер объявления, которое хочешь удалить')
    else:
        await message.answer('У вас недостаточно прав для этой операции(')

@dp.message_handler(state=Delete_ads.num_ads)
async def load_num(message: types.Message, state: FSMContext):
    await message.answer(str(delete_ads(int(message.text))))
    await state.finish()

@dp.message_handler(commands=['deleteadsall'])
async def delete_ads_all_cmd(message: types.Message):
    if message.from_user.id == admin_id:
        await delete_all_ads()
    else:
        await message.answer('У вас недостаточно прав для этой операции(')


#######################################   создание напоминания   ####################################
@dp.message_handler(Text(equals='Создать напоминание', ignore_case=True), state = None)
async def start_com(message: types.Message):
    global count_desc
    if message.from_user.id != admin_id:    #проверка на админа
        await message.answer("У вас недостаточно прав для этой операции")
        return 0
    if count_desc == 0:
        await message.answer(text=DESC_REMINDER)
        count_desc += 1
    await question.q1.set()
    await message.answer(text="Введите напоминание")

@dp.message_handler(state = question.q1)
async def que1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['q1'] = message.text
    await question.next()
    await message.answer(text="Введите дату напоминания в формате ДД/ММ/ГГ ЧЧ:ММ (Пр: 01/01/22 09:45)")

@dp.message_handler(state = question.q2)
async def que2(message: types.Message, state: FSMContext):
    global group_id
    global count_answer
    count_answer = 0
    async with state.proxy() as data:
        try:
            date_time = datetime.datetime.strptime(message.text, "%d/%m/%y %H:%M")
            dtp = date_time.timestamp() #планируемая дата в секундах

            today = datetime.datetime.today()
            dty = datetime.datetime.today().timestamp()  # текущая дата в секундах

            if dty >= dtp:
                await message.answer(
                    text="Ошибка, введите корректную дату")  # проверка на прошедшую дату
                return 0

        except:
            await message.answer(text="Ошибка, введите корректную дату")
            return 0

    await state.finish()

    await message.answer(text="Напоминание создано")

    delta_s = int(dtp - dty - 1) #разница дат в секундах

    await asyncio.sleep(delta_s) #функция неактивна, пока разница между датами не равна 0

    today = datetime.datetime.today()

    while True:
        if date_time > today:
            today = datetime.datetime.today()
        else:
            await bot.send_message(chat_id=group_id,
                                   text=data['q1'])
            break


#######################################   Реакция на неопознанную команду   ####################################
@dp.message_handler()
async def not_command(message: types.Message):
    global group_id
    global count_zp
    if message.chat.id != group_id:
        await bot.send_sticker(message.chat.id, sticker="CAACAgIAAxkBAAEGbrljc8C0JFrg7ORz_e3KDUSA-PwJLwACoCEAAuiCoUt66qBRIJCCSisE")
    else:
        if message.text[0] == '*':
            if count_zp < 10:
                answer_question(user_id=message.from_user.id, count_zp=count_zp)
                await bot.send_message(message.from_user.id, text='Вам начислено 10 баллов за ответ на вопрос!')
            else:
                await bot.send_message(message.from_user.id, text="Вы уже получили награду за этот вопрос")
            count_zp += 1

if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)