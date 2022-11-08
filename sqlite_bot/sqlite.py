import sqlite3 as sq
from fuzzywuzzy import fuzz

#функция, создающая базу данных
async def db_start():
    global db, cursor

    db = sq.connect('ankets.db')
    cursor = db.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS profile(user_id TEXT PRIMARY KEY, photo TEXT, name TEXT, age TEXT, description TEXT, url_tg TEXT, score TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS ads(number TEXT PRIMARY KEY, photo TEXT, description TEXT, price TEXT, count TEXT)')
    db.commit()

#создаие шаблона под одно объявление
async def create_ads(count_ad):
    cursor.execute('INSERT INTO ads VALUES(?, ?, ?, ?, ?)', (count_ad, '', '', '', ''))
    db.commit()


#создаем профиль (таблица с колонками id, фото, имя, возраст, описание)
async def create_profile(user_id):
    user = cursor.execute('SELECT * FROM profile WHERE user_id == {key}'.format(key=user_id)).fetchone()
    if not user:
        cursor.execute('INSERT INTO profile VALUES(?, ?, ?, ?, ?, ?, ?)', (user_id, '', '', '', '', '', ''))
        db.commit()

#добавление объявления
async def edit_ads(state, count_ad):
    async with state.proxy() as data:
        cursor.execute("UPDATE ads SET photo = '{}', description = '{}', price = '{}', count = '{}' WHERE number = '{}'".format(
            data['photo_ads'],
            data['desc_ads'],
            data['price_ads'],
            data['count_product_ads'],
            count_ad
        ))
        db.commit()

#добавление профиля, если такого не существует
async def edit_profile(state, user_id, score):
    async with state.proxy() as data:
        cursor.execute("UPDATE profile SET photo = '{}', name = '{}', age = '{}', description = '{}', url_tg = '{}', score = {}  WHERE user_id = '{}' ".format(
            data['photo'],
            data['name'],
            data['age'],
            data['desc'],
            data['url_tg'],
            score,
            user_id
        ))
        db.commit()

#рекомендация пользователя(выбор строки о пользоватле из БД)
def rec(user_id, count):
    users = cursor.execute('SELECT user_id FROM profile').fetchall()    #вложенные кортежи с id всех пользователей бота, сохранивших анкету
    users_list = []     #список с id всех пользователей
    rec_user = []       #список в котором будуд лежать данные о конкретном пользователе
    desc_users = []
    reyting_users = []

    for i in users:
        users_list.append(int(i[0]))
    users_list.remove(user_id)
    if users_list == []:
        return 'Кроме вас пока что никого нет'

    user_desc = cursor.execute('SELECT description FROM profile WHERE user_id == {key}'.format(key=user_id)).fetchone()[0]

    for i in users_list:
        desc_users.append(cursor.execute('SELECT description FROM profile WHERE user_id == {key}'.format(key=i)).fetchone()[0])

    for i in range(len(desc_users)):
        reyting_users.append(0)

    for i in desc_users:
        reyting_users[desc_users.index(i)] = fuzz.WRatio(user_desc, i)

    for i in range(len(reyting_users) - 1):
        for j in range(len(reyting_users) - 2, i - 1, -1):
            if reyting_users[j + 1] < reyting_users[j]:
                reyting_users[j], reyting_users[j+1] = reyting_users[j+1], reyting_users[j]
                users_list[j], users_list[j+1] = users_list[j+1], users_list[j]
    users_list.reverse()

    if len(users_list) > count:     #проверка, прошли ли все анкеты или нет
        rec_user_id = users_list[count] #id рекомендуемого пользователя
        rec_user_inf = cursor.execute('SELECT * FROM profile WHERE user_id == {key}'.format(key=rec_user_id)).fetchone()   #получение остальных данных рекомендуемого пользователя
        for j in rec_user_inf:
            rec_user.append(j)

        return rec_user

    else:
        return 'Ты посмотрел все анкеты, которые есть, теперь они пойдут заново'

#рекомендация объявлений
def rec_ads(count_ads):
    ads = cursor.execute('SELECT number FROM ads').fetchall() #все номера объявлений
    ads_list = []   #список из номеров объяявлений
    ad = []    #список с информацией о конкретном объявлении
    for i in ads:
        ads_list.append(int(i[0]))

    if ads_list == []:
        return 'Пока что нет объявлений'

    if len(ads_list) > count_ads:
        ad_rec = ads_list[count_ads]
        ad_inf = cursor.execute('SELECT * FROM ads WHERE number == {key}'.format(key=ad_rec)).fetchone()
        for i in ad_inf:
            ad.append(i)
        return ad
    else:
        return 'Ты посмотрел все объявления, теперь они пойдут заново'

def change_data(count_ads, user_id):
    price = cursor.execute('SELECT price FROM ads WHERE number == {key}'.format(key=count_ads)).fetchone()
    now_score = int(cursor.execute('SELECT score FROM profile WHERE user_id == {key}'.format(key=user_id)).fetchone()[0])
    cursor.execute('UPDATE profile SET score = "{}" WHERE user_id = {}'.format(str(now_score - int(price[0])), user_id))
    db.commit()

def price(count_ads):
    price = cursor.execute('SELECT price FROM ads WHERE number == {key}'.format(key=count_ads)).fetchone()
    return int(price[0])




#обновление количества очков при ответе на вопрос
def answer_question(user_id, count_zp):
    if count_zp == 0:
        now_score = int(cursor.execute('SELECT score FROM profile WHERE user_id == {key}'.format(key=user_id)).fetchone()[0])
        cursor.execute('UPDATE profile SET score = "{}" WHERE user_id = {} '.format(str(now_score + 10), user_id))
        db.commit()

#трата баллов
def waste(user_id):
    now_score = int(cursor.execute('SELECT score FROM profile WHERE user_id == {key}'.format(key=user_id)).fetchone()[0])
    cursor.execute('UPDATE profile SET score = "{}" WHERE user_id = {}'.format(str(now_score - 10), user_id))
    db.commit()

#первое пополнение при вызове команды /start
def first_salary(user_id):
    start_summ = 50
    cursor.execute('UPDATE profile SET score = "{}" WHERE user_id = {}'.format(start_summ, user_id))
    db.commit()

#обращение к бд за информацией о балансе
def balans_inf(user_id):
    inf = int(cursor.execute('SELECT score FROM profile WHERE user_id == {key}'.format(key=user_id)).fetchone()[0])
    return inf

#удаление профиля
async def delete_profile(user_id):
    cursor.execute('DELETE from profile WHERE user_id == {key}'.format(key=user_id))
    db.commit()

#удаление объявления
async def delete_ads(count_ad):
    cursor.execute('DELETE from ads WHERE number == {key}'.format(key=count_ad))
    db.commit()
async def delete_all_ads():
    cursor.execute("DELETE from ads")
    db.commit()