import sqlite3 as sq

#функция, создающая базу данных
async def db_start():
    global db, cursor

    db = sq.connect('ankets.db')
    cursor = db.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS profile(user_id TEXT PRIMARY KEY, photo TEXT, name TEXT, age TEXT, description TEXT)')
    db.commit()

#создаем профиль (таблица с колонками id, фото, имя, возраст, описание)
async def create_profile(user_id):
    user = cursor.execute('SELECT 1 FROM profile WHERE user_id == {key}'.format(key=user_id)).fetchone()
    if not user:
        cursor.execute('INSERT INTO profile VALUES(?, ?, ?, ?, ?)', (user_id, '', '', '', ''))
        db.commit()

#добавление профиля, если такого не существует
async def edit_profile(state, user_id):
    async with state.proxy() as data:
        cursor.execute("UPDATE profile SET photo = '{}', name = '{}', age = '{}', description = '{}' WHERE user_id = '{}' ".format(
            data['photo'],
            data['name'],
            data['age'],
            data['desc'],
            user_id
        ))
        db.commit()

#удаление профиля
async def delete_profile(user_id):
    cursor.execute('DELETE from profile WHERE user_id == {key}'.format(key=user_id))
    db.commit()
