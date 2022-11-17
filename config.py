API_TOKEN = '5656646184:AAFxzPdfu-aEdBQZDftJB1MGTauT6IWVF1o'

START = '''
Что умеет этот бот?
Бот, основываясь на схожих интересах, предложит  Вам сотрудника из компании для дальнейшего общения!
Создайте анкету и начинайте общение!
'''

START_ADMIN = '''
Привет, так как ты админ, для тебя будет немного другой функционал)
'''

HELP_LIST = '''
<b>/start</b><em> - начать работу</em>
<b>/help</b><em> - список команд</em>
<b>/description</b><em> - описание бота</em>
<b>/feedback</b><em> - отправить отзыв о работе бота</em>
<b>/deleteprofile</b><em> - удаление профиля</em>
<b>Найти друга</b><em> - рекомендация</em>
<b>Заполнить анкету!</b><em> - начать заполнение анкеты</em>
<b>Мой баланс</b><em> - узнать баланс</em>
<b>Войти</b><em> - авторизация администратора</em>
'''

#<b></b><em></em>
HELP_ADMIN_LIST = '''
<b>/start</b><em> - начать работу</em>
<b>/help</b><em> - список команд</em>
<b>/description</b><em> - описание бота</em>
<b>/feedback</b><em> - отправить отзыв о работе бота</em>
<b>/deleteprofile</b><em> - удаление профиля</em>
<b>Найти друга</b><em> - рекомендация</em>
<b>Заполнить анкету!</b><em> - начать заполнение анкеты</em>
<b>Мой баланс</b><em> - узнать баланс</em>
<b>Войти</b><em> - авторизация администратора</em>
<b>Сменить пароль</b><em> - смена пароля</em>
<b>Создать объявление</b><em> - заполнить объявление с товаром</em>
<b>начислить баллы</b><em> - начислить баллы любому пользователю, имеющему анкету,  по его имени</em>
<b>/deleteads</b><em> - удалить объявление по его номеру</em>
<b>/deleteadsall</b><em> - удалить ВСЕ объявления из базы данных</em>
<b>Клавиатура пользователь</b><em> - переводит вас на телеграм-клавиатуру(кнопки) для обычного пользователя</em>
<b>Клавиатура админ</b><em> - возвращает вас на клавиатуру для админа</em>
<b>Получить базу данных</b><em> - бот пришлет вам файл формата txt со всей информацией о профилях пользователей</em>
'''

DESCRIPTION = '''
Бот для поиска собеседников с похожими интересами из вашей же компании!
'''

DESC_REMINDER = '''
Это сообщение появляется только при первом запуске бота или после его перезагрузки!
Данная функция может создать несколько напоминаний в группе, которые появятся в определённое время. 
До первого создания напоминания (после первого запуска бота или перезапуска) необходимо написать команду 
"/start_remind" в той группе, где нужно создать напоминание, чтобы бот запомнил id чата, далее "/start_remind" можно не писать.
Важно! При перезапуске бота напоминания стираются.
Важно! Любые напоминания не текстового формата (фото, видео, стикеры и т.д.) будут проигнорированы
'''

sticker_id = [
    'CAACAgIAAxkBAAEGdVJjdqB8T-QM0IwD0uwrnmuBvAoHPQACQyUAAlwwoUsLBOymdCE4hysE',
    'CAACAgIAAxkBAAEGdVRjdqCQ9zUK3UAwm2OFlWJLKFJqUAACoSIAAt33oEtnl1fTKgcu9isE',
    'CAACAgIAAxkBAAEGdVZjdqCrBo85RGcZIGErnzsYzstMJAACWykAAi01oUvpFH7AujT7kCsE',
    'CAACAgIAAxkBAAEGdVpjdqDB1dWNc_vxG_GE740NNoHWfgACoCEAAuiCoUt66qBRIJCCSisE',
    'CAACAgIAAxkBAAEGdVxjdqDV7r3QmcfBZzne8Y5PlWMAAcgAAn4hAAKj9qBLSxPVGInbQZkrBA',
    'CAACAgIAAxkBAAEGdWBjdqD_YmHBllmoF1zVvkhYKN5eeAACpR0AArFpoEvs_tAZAQwhJysE',
    'CAACAgIAAxkBAAEGdWJjdqEIt18IXDJgApSGVRxNT5KTgQACyCMAAnOXoUul5AQF2oPjpCsE'
]