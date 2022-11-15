import sqlite3 as sq
from fuzzywuzzy import fuzz

#функция, создающая базу данных
async def db_start():
    global db, cursor

    db = sq.connect('ankets.db')
    cursor = db.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS profile(user_id TEXT PRIMARY KEY, photo TEXT, name TEXT, age TEXT, description TEXT, url_tg TEXT, score TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS ads(number TEXT PRIMARY KEY, photo TEXT, description TEXT, price TEXT, count TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS password(num TEXT PRIMARY KEY, pass TEXT)')
    db.commit()

#создаие шаблона под одно объявление
async def create_ads():
    numbers = cursor.execute('SELECT number FROM ads').fetchall()
    numbers_list = []
    for i in numbers:
        numbers_list.append(int(i[0]))
    if numbers_list == []:
        cursor.execute('INSERT INTO ads VALUES(?, ?, ?, ?, ?)', (1, '', '', '', ''))
        db.commit()
    else:
        cursor.execute('INSERT INTO ads VALUES(?, ?, ?, ?, ?)', (int(numbers_list[-1]) + 1, '', '', '', ''))
        db.commit()

#создание бд с паролем
async def create_password():
    pass_chek = cursor.execute("SELECT num FROM password").fetchall()
    pass_chek_list = []

    for i in pass_chek:
        pass_chek_list.append(i[0])

    if pass_chek_list == []:
        print('test1')
        cursor.execute('INSERT INTO password VALUES(?, ?)', (1, 'admin'))
        db.commit()

# смена пароля в бд
def change_password(password):
    cursor.execute('UPDATE password SET pass = "{}" WHERE num == {}'.format(password, str(1)))
    db.commit()
    return 'Пароль успешно изменен!'

#текущий пароль
def current_pass():
    return cursor.execute('SELECT pass FROM password WHERE num == {key}'.format(key=1)).fetchone()[0]

#создаем профиль (таблица с колонками id, фото, имя, возраст, описание)
async def create_profile(user_id):
    user = cursor.execute('SELECT * FROM profile WHERE user_id == {key}'.format(key=user_id)).fetchone()
    if not user:
        cursor.execute('INSERT INTO profile VALUES(?, ?, ?, ?, ?, ?, ?)', (user_id, '', '', '', '', '', ''))
        db.commit()
count_test = 0

#добавление объявления
async def edit_ads(state):
    global count_test
    numbers = cursor.execute('SELECT number FROM ads').fetchall()
    numbers_list = []
    for i in numbers:
        numbers_list.append(int(i[0]))
    async with state.proxy() as data:
        cursor.execute(
            "UPDATE ads SET photo = '{}', description = '{}', price = '{}', count = '{}' WHERE number = '{}'".format(
                data['photo_ads'],
                data['desc_ads'],
                data['price_ads'],
                data['count_product_ads'],
                numbers_list[-1]
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



def all_db():
    data_base = cursor.execute('SELECT name, age, description, url_tg FROM profile').fetchall()
    return data_base


#получение значения цены для конкретного товара
def price(count_ads):
    global price
    ads = cursor.execute('SELECT number FROM ads').fetchall()  # все номера объявлений
    ads_list = []  # список из номеров объяявлений
    for i in ads:
        ads_list.append(int(i[0]))
    len(ads_list)
    price = cursor.execute('SELECT price FROM ads WHERE number == {key}'.format(key=str(ads_list[count_ads]))).fetchone()
    return int(price[0])

#изменение информации о баллах в бд после покупки
def change_data(count_ads, user_id):
    global price
    now_score = int(cursor.execute('SELECT score FROM profile WHERE user_id == {key}'.format(key=user_id)).fetchone()[0])
    cursor.execute('UPDATE profile SET score = "{}" WHERE user_id = {}'.format(str(now_score - int(price[0])), user_id))
    db.commit()

#получение имени пользователя с заданным id
def name(user_id):
    name = cursor.execute('SELECT name FROM profile WHERE user_id == {key}'.format(key=user_id)).fetchone()
    if name is None:
        return 'Вы не авторизованы, заполните анкету'
    else:
        return name[0]

def tg_url(user_id):
    tg = cursor.execute('SELECT url_tg FROM profile WHERE user_id == {key}'.format(key=user_id)).fetchone()
    return tg[0]

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
    start_summ = 100
    cursor.execute('UPDATE profile SET score = "{}" WHERE user_id = {}'.format(start_summ, user_id))
    db.commit()

#начисление заданного кол-ва баллов конкретному пользоватлею
def salary(user_id, summ):
    now_score = int(cursor.execute('SELECT score FROM profile WHERE user_id == {key}'.format(key=user_id)).fetchone()[0])
    cursor.execute('UPDATE profile SET score = "{}" WHERE user_id = {}'.format(str(now_score + summ), user_id))
    db.commit()

#поиск пользователя в бд по его имени
def find_user(name_user):
    users = cursor.execute('SELECT user_id FROM profile').fetchall()

    users_list = []
    name_users = []
    f_name = False
    for i in users:
        users_list.append(int(i[0]))
    for i in users_list:
        name_users.append(cursor.execute('SELECT name FROM profile WHERE user_id == {key}'.format(key=i)).fetchone()[0])
    for i in name_users:
        if i == name_user:
            f_name = True
            return users_list[name_users.index(i)]
    if f_name == False:
        return 'Пользователь не найден'

#обращение к бд за информацией о балансе
def balans_inf(user_id):
    inf = cursor.execute('SELECT score FROM profile WHERE user_id == {key}'.format(key=user_id)).fetchone()
    if inf is None:
        return -1
    else:
        return int(inf[0])

#удаление профиля
async def delete_profile(user_id):
    cursor.execute('DELETE from profile WHERE user_id == {key}'.format(key=user_id))
    db.commit()

#изменение количества товара
async def count_product(count_ads):
    ads = cursor.execute('SELECT number FROM ads').fetchall()  # все номера объявлений
    ads_list = []  # список из номеров объяявлений
    for i in ads:
        ads_list.append(int(i[0]))
    count = cursor.execute('SELECT count FROM ads WHERE number == {key}'.format(key=str(count_ads))).fetchone()
    if int(count[0]) == 1:
        delete_ads(count_ads)
    else:
        cursor.execute('UPDATE ads SET count = "{}" WHERE number == {}'.format(str(int(count[0]) - 1), count_ads))
        db.commit()

#получение номера товара
def num(count_ads):
    ads = cursor.execute('SELECT number FROM ads').fetchall() #все номера объявлений
    ads_list = []   #список из номеров объяявлений
    for i in ads:
        ads_list.append(int(i[0]))

    if len(ads_list) > count_ads:
        ad_rec = ads_list[count_ads]
        return ad_rec


#удаление объявления
def delete_ads(count_ad):
    ads = cursor.execute('SELECT number FROM ads').fetchall()
    ads_list = []
    f_num = False
    for i in ads:
        ads_list.append(i[0])
    for i in ads_list:
        if int(i) == count_ad:
            cursor.execute('DELETE from ads WHERE number == {key}'.format(key=count_ad))
            db.commit()
            f_num = True
            return 'Объявление удалено'
    if not (f_num):
       return "Объявления с таким номером не существует"

#получение списка текущих номеров объявлений
def num_current_ads():
    ads = cursor.execute('SELECT number FROM ads').fetchall()
    ads_list = []
    for i in ads:
        ads_list.append(i[0])
    return int(ads_list[-1])

#удаление ВСЕХ объявлений
async def delete_all_ads():
    cursor.execute("DELETE from ads")
    db.commit()