import sqlite3 as sq
from random import randint

#функция, создающая базу данных
async def db_start():
    global db, cursor

    db = sq.connect('ankets.db')
    cursor = db.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS profile(user_id TEXT PRIMARY KEY, photo TEXT, name TEXT, age TEXT, description TEXT, url_tg TEXT)')
    db.commit()

#создаем профиль (таблица с колонками id, фото, имя, возраст, описание)
async def create_profile(user_id):
    user = cursor.execute('SELECT 1 FROM profile WHERE user_id == {key}'.format(key=user_id)).fetchone()
    if not user:
        cursor.execute('INSERT INTO profile VALUES(?, ?, ?, ?, ?, ?)', (user_id, '', '', '', '', ''))
        db.commit()

#добавление профиля, если такого не существует
async def edit_profile(state, user_id):
    async with state.proxy() as data:
        cursor.execute("UPDATE profile SET photo = '{}', name = '{}', age = '{}', description = '{}', url_tg = '{}' WHERE user_id = '{}' ".format(
            data['photo'],
            data['name'],
            data['age'],
            data['desc'],
            data['url_tg'],
            user_id
        ))
        db.commit()

#рекомендация пользователя(выбор строки о пользоватле из БД)
def rec(user_id, count):
    users = cursor.execute('SELECT user_id FROM profile').fetchall()    #вложенные кортежи с id всех пользователей бота, сохранивших анкету
    users_list = []     #массив со списком id всех пользователей
    rec_user = []       #массив в котором будуд лежать данные о конкретном пользователе

    for i in users:
        users_list.append(int(i[0]))
    users_list.remove(user_id)
    if users_list == []:
        return 'Кроме вас пока что никого нет'
    if len(users_list) > count:     #проверка, прошли ли все анкеты или нет
        rec_user_id = users_list[count] #id рекомендуемого пользователя
        rec_user_inf = cursor.execute('SELECT * FROM profile WHERE user_id == {key}'.format(key=rec_user_id)).fetchone()   #получение остальных данных рекомендуемого пользователя
        for j in rec_user_inf:
            rec_user.append(j)
        return rec_user

    else:
        return 'Ты посмотрел все анкеты, котрые есть, теперь они пойдут заново'


#удаление профиля
async def delete_profile(user_id):
    cursor.execute('DELETE from profile WHERE user_id == {key}'.format(key=user_id))
    db.commit()
