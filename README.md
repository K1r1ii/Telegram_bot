# <a href='https://t.me/corparateBot'>Corparate Bot</a>
## Описание
Corporate bot - это чат-бот для тимбиллинга, который имеет встроенную игровую механику: сотрудники компании мотивируются к общению за счёт внутриигровой валюты, таким образом, достигается максимальная вовлечённость и заинтересованность. Помимо этого, наш бот умеет создавать анкеты для знакомств, а так же  рекомендовать анкеты других пользователей, исходя из общих интересов. Мы уверены, что за счёт предлагаемых инструментов, сотрудники компаний могут развить между собой доверительные, дружеские отношения, тем самым, значительно увеличив эффективность работы коллектива.
## Структура репозитория
- <a href='https://github.com/K1r1ii/Telegram_bot/blob/TelegramBot_/start/Bot_anketa.py'>Bot_anketa.py</a> - файл с основным кодом проекта
- <a href='https://github.com/K1r1ii/Telegram_bot/blob/TelegramBot_/start/config.py'>config.py</a> - файл с текстами(токен, описание, start, help)
- <a href='https://github.com/K1r1ii/Telegram_bot/blob/TelegramBot_/start/keyboards.py'>keyboards.py</a> - файл для работы с клавиатурами бота
- <a href='https://github.com/K1r1ii/Telegram_bot/tree/TelegramBot_/start/sqlite_bot'>sqlite_bot</a> -> <a href='https://github.com/K1r1ii/Telegram_bot/blob/TelegramBot_/start/sqlite_bot/sqlite.py'>sqlite.py</a> - файл для работы с базой данных
- <a href='https://github.com/K1r1ii/Telegram_bot/blob/TelegramBot_/start/ankets.db'>ankets.db</a> - база данных
- <a href='https://github.com/K1r1ii/Telegram_bot/blob/TelegramBot_/start/all_db.txt'>all_db.txt</a> - текстовый файл, который отправляется админу, в нем содержится актуальная информация из базы данных
- <a href='https://github.com/K1r1ii/Telegram_bot/tree/TelegramBot_/start/bot_scrin'>bot_scrin</a> - файл со скринами бота
- <a href='https://github.com/K1r1ii/Telegram_bot/tree/TelegramBot_/start/архитектура%20бота'>архитектура бота</a> - файл со схемами архитектуры
- <a href='https://github.com/K1r1ii/Telegram_bot/blob/TelegramBot_/start/requirements.txt'>requirements.txt</a> - файл с зависимостями
## фичи
- Возможность создавать свою анкету с фото, описанием, именем и возрастом.
- Внутриигровая валюта: стартовый капитал пользователь получает при создании анкеты.
- Просмотр других анкет, которые появляются в определенном порядке, выстраиваясь так, что первой будет анкета наиболее схожая с описанием пользователя, за получение анкеты взимается оплата внутриигровой валютой.
- Бот в общем чате: бот задает вопросы, созданные HR два раза в день, за ответ на вопрос, пользователь получает валюту + уведомление об этои в лс.
- Аккаунт администратора: возможность создать профиль HR, со спец возможностями, такими как составление вопросов для бота(фича выше), награждение пользоватлей валютой, создание объявлений(слудующая фича), доступ к бд.
- Магазин объявлений: HR создает объявление, также как создают анкету, и оно попадает в список объявлений, которые пользователи могут просмотреть и купить, если у них хватает валюты. Товарами могут быть мерч, подарки, сертификаты, премии, бонусы и все, что сделает HR.
## стек
1. <a href="https://www.python.org/">Python3</a> - язык программирования.
2. <a href="https://www.jetbrains.com/pycharm/">Pycharm</a> - среда разработки.
3. <a href="https://github.com/aiogram/aiogram">Aiogram</a> - библиотека для создания телеграм бота.
4. <a href="https://www3.sqlite.org/index.html">SQLite</a> - база данных для хранения информации о пользователях.
5. <a href="https://pythonru.com/osnovy/sqlite-v-python">SQLite3</a> - библиотека для работы с sqlite.
6. <a href="https://pypi.org/project/fuzzywuzzy/">Fuzzywuzzy</a> - библиотека для быстрого сравнения текстов.
## Архитектура
### Пользовательский интерфейс
<img src="https://github.com/K1r1ii/Telegram_bot/blob/TelegramBot_/start/архитектура%20бота/архитектура_пользователь.png">

### Интерфейс администратора
<img src="https://github.com/K1r1ii/Telegram_bot/blob/TelegramBot_/start/архитектура%20бота/админ_архитектура.png">

### Другие функции
<img src="https://github.com/K1r1ii/Telegram_bot/blob/TelegramBot_/start/архитектура%20бота/другие%20команды.png">

## Запуск бота
- установите все зависимости из файла requirements.txt
- Запустите файл Bot_anketa.py
- Тестируйте по ссылке https://t.me/corparateBot
## Команда
- Юлия Пятакова - менеджер(@Julia_Pyatakova)
- Анастасия Бурматнова - маркетолог(@NastyaBurmatnova)
- Никита Абрамов - дизайнер(@narcoOilOFTmin)
- Дмитрий Скороходов - backend-программист(@dimask13)
- Сальников Кирилл - backend-программист(@Klr11111)
## фото проекта

### Создание анкеты
<img src="https://github.com/K1r1ii/Telegram_bot/blob/TelegramBot_/start/bot_scrin/создание%20анкеты.png">

### Анкета
<img src="https://github.com/K1r1ii/Telegram_bot/blob/TelegramBot_/start/bot_scrin/анкета.png">

### Ответ на вопрос
<img src="https://github.com/K1r1ii/Telegram_bot/blob/TelegramBot_/start/bot_scrin/Снимок%20экрана%20(28).png">

### Проверка баланса
<img src="https://github.com/K1r1ii/Telegram_bot/blob/TelegramBot_/start/bot_scrin/Снимок%20экрана%20(30).png">

### Объявление
<img src="https://github.com/K1r1ii/Telegram_bot/blob/TelegramBot_/start/bot_scrin/объявление.png">

### Уведомление о покупке, приходящее пользователю
<img src="https://github.com/K1r1ii/Telegram_bot/blob/TelegramBot_/start/bot_scrin/скрин%20покупки%20товара%20пользователь.jpg">

### Уведомление о покупке, приходящее администратору
<img src="https://github.com/K1r1ii/Telegram_bot/blob/TelegramBot_/start/bot_scrin/уведомление%20о%20покупке%20товара%20у%20админа.png">



