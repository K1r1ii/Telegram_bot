from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from keyboards import get_keyboard, get_inline_keyboard, get_cancel
from config import *
from sqlite_bot.sqlite import db_start, create_profile, edit_profile, delete_profile

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


#действия при команде старт
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message) -> None:
    await message.answer(text = "Привет, я бот из команды /start!", reply_markup=get_keyboard())
    await message.delete()
    await create_profile(user_id=message.from_user.id)

#отмена заполнения анкеты, сброс состояний
@dp.message_handler(commands=['cancel'], state='*')
async def cancel_command(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.answer(text='Заполнение анкеты отменено',
                         reply_markup=get_keyboard())
    await delete_profile(user_id=message.from_user.id)
    await state.finish()

#функция удаления профиля
@dp.message_handler(commands=['DeleteProfile'])
async def delete_command(message: types.Message):
    await delete_profile(user_id=message.from_user.id)
    await message.answer(text='Ваша анкета удалена')

#начинаем создавать анкету
@dp.message_handler(Text(equals='Заполнить анкету!', ignore_case=True), state=None)
async def start_anketa(message: types.Message,  state: FSMContext) -> None:
    await Anketa_states_group.photo.set()
    await message.answer('Отправь свое фото!', reply_markup=get_cancel())

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
    await message.answer('Теперь напиши свое имя)')

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
    async with state.proxy() as data:
        await bot.send_photo(message.from_user.id,
                             photo=data['photo'],
                             caption=f'{data["name"]}, {data["age"]}\n{data["desc"]}')
    await edit_profile(state, user_id=message.from_user.id)
    await state.finish()

# #вызов функционала бота
# @dp.message_handler(commands=['help'])
# async def help_command(message: types.Message):
#     await message.reply(HELP_LIST, parse_mode='HTML')
#
# #вызов описания бота
# @dp.message_handler(commands=['description'])
# async def description_command(message: types.Message):
#     await message.answer(DESCRIPTION)
#     await message.delete()

if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)