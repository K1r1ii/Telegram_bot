from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from keyboards import *
from config import *
from sqlite_bot.sqlite import *

#запуск базы данных(создание)
async def on_startup(_):
    await db_start()

#создания экземпляра бота, диспетчера, и состояний
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot= bot, storage=storage)

#значения, которые будут задваться с аккаунта администратора
start_score = 10
question_text = 'Как прошел твой день?'

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

#######################################   Обработчики вспомогательных команд   ####################################
#действия при команде старт
count_start = 0
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message) -> None:
    global count_start
    if count_start == 0:
        first_salary(user_id=message.from_user.id)
        count_start += 1
    await message.answer(text = START, reply_markup=get_keyboard())
    await message.delete()

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
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.answer(text='Заполнение объявления отменено',
                         reply_markup=get_keyboard())
    await delete_ads(count_ad=count_ad)
    await state.finish()

#функция удаления объявления
@dp.message_handler(commands=['deleteads'])
async def delete_command_ads(message: types.Message):
    global count_ad
    await delete_ads(count_ad=count_ad)
    await message.answer(text='Ваше объявление удалено',
                         reply_markup=get_keyboard())
    count_ad = 0

#функция удаления профиля
@dp.message_handler(commands=['deleteprofile'])
async def delete_command(message: types.Message):
    await delete_profile(user_id=message.from_user.id)
    await message.answer(text='Ваша анкета удалена',
                         reply_markup=get_keyboard())

#вызов функционала бота
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
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



#######################################   Рекомендации   ####################################
#функция, отвечающая за рекомендации другим пользователям
#счетчик count нужен для того, чтобы избежать отправки анкеты, которая уже была отправлена
count = 0
count_zp = 0
@dp.message_handler(Text(equals='Найти друга!', ignore_case=True))
async def rec_command(message: types.Message):
    global count
    now_balans = balans_inf(user_id=message.from_user.id)
    if now_balans >= start_score:
        waste(user_id=message.from_user.id)
        await bot.send_message(message.from_user.id, text='С вашего счета списано 10 валют!')
        if type(rec(user_id=message.from_user.id, count=count)) == str:     #если мы отправляем строку, значит дошли до конца в списке анкет, предупреждаем польхователя, обнуляем счетчик и начинаем сначала
            await message.answer(text=rec(user_id=message.from_user.id, count=count))
            count = 0
        else:   #если тип не строчный(массив), то собираем и отправляем анкету, увеличивая счетчик
            m = rec(user_id=message.from_user.id, count=count)
            await bot.send_photo(message.from_user.id,
                                 photo=m[1],
                                 caption=f'{m[2]}, {m[3]}\n{m[4]}',
                                 reply_markup=get_inline_keyboard_rec(m[5]))
            count += 1
    else:
        await bot.send_message(message.from_user.id, text='На счету не хватает денег, видимо пора отвечать на вопросы в общем чате!')

#######################################   Создание объявления   ####################################
count_ad = 0
@dp.message_handler(Text(equals='Объявление', ignore_case=True), state=None)
async def start_ad(message: types.Message, state: FSMContext) -> None:
    global count_ad
    count_ad += 1
    await Ads_states_group.photo.set()
    await create_ads(count_ad=count_ad)
    await message.answer('Отправь фото товара(услуги)', reply_markup=get_cancel_ads())

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
    await message.answer(text='Объявление готово')
    await bot.send_photo(message.from_user.id,
                         photo=data['photo_ads'],
                         caption=f'{data["desc_ads"]}\nЦена: {data["price_ads"]}\nКоличество: {data["count_product_ads"]}'
                         )
    await edit_ads(state, count_ad=count_ad)
    await state.finish()




#######################################   Создание Анкеты   ####################################

#начинаем создавать анкету
@dp.message_handler(Text(equals='Заполнить анкету', ignore_case=True), state=None)
async def start_anketa(message: types.Message,  state: FSMContext) -> None:
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


#######################################   Бот для общего чата(не доделано)   ####################################
#функция для приема ответов пользователя, ответ дается с спецсимволом в начале
@dp.message_handler()
async def answer(message: types.Message):
    global count_zp
    if message.text[0] == '*':
        if count_zp == 0:
            answer_question(user_id=message.from_user.id, count_zp=count_zp)
            await bot.send_message(message.from_user.id, text='Вам начислено 10 баллов за ответ на вопрос!')
        else:
            await bot.send_message(message.from_user.id, text="Вы уже получили награду за этот вопрос")
        count_zp += 1

if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)