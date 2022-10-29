from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from keyboards import get_keyboard, get_inline_keyboard_feedback, get_cancel, get_inline_keyboard_rec
from config import *
from sqlite_bot.sqlite import db_start, create_profile, edit_profile, delete_profile, rec

async def on_startup(_):
    await db_start()

#создания экземпляра бота, диспетчера, и состояний
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot= bot, storage=storage)

#создание класса для состояний
class Anketa_states_group(StatesGroup):
    photo = State()
    name = State()
    age = State()
    desc = State()
    url_tg = State()


#действия при команде старт
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message) -> None:
    await message.answer(text = START, reply_markup=get_keyboard())
    await message.delete()


#отмена заполнения анкеты, сброс состояний
@dp.message_handler(Text(equals='Отменить заполнение', ignore_case=True), state='*')
async def cancel_command(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.answer(text='Заполнение анкеты отменено',
                         reply_markup=get_keyboard())
    await delete_profile(user_id=message.from_user.id)
    await state.finish()

#функция удаления профиля
@dp.message_handler(commands=['deleteprofile'])
async def delete_command(message: types.Message):
    await delete_profile(user_id=message.from_user.id)
    await message.answer(text='Ваша анкета удалена',
                         reply_markup=get_keyboard())



#функция, отвечающая за рекомендации другим пользователям
#счетчик count нужен для того, чтобы избежать отправки анкеты, которая уже была отправлена
count = 0
@dp.message_handler(Text(equals='Найти друга!', ignore_case=True))
async def rec_command(message: types.Message):
    global count
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

#начинаем создавать анкету
@dp.message_handler(Text(equals='Заполнить анкету', ignore_case=True), state=None)
async def start_anketa(message: types.Message,  state: FSMContext) -> None:
    await Anketa_states_group.photo.set()
    await create_profile(user_id=message.from_user.id)
    await message.answer('Отправь мне свое фото', reply_markup=get_cancel())

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
    await edit_profile(state, user_id=message.from_user.id)
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)