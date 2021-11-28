<h2>Тестовое задание для компании KVINT</h2>
Реализован чат-бот для обработки заказа пиццы.

Бот доступен по ссылке [https://t.me/KvintPizzaRobot](https://t.me/KvintPizzaRobot)

В файле [conversation_handler.py](https://github.com/Ilia-Abrosimov/KVINT_Chat_Bot/blob/master/conversation_handler.py) бот реализован через класс ConversationHandler встроенный в библиотеку python-telegram-bot, который также использует стейт машину.
В файле [main.py](https://github.com/Ilia-Abrosimov/KVINT_Chat_Bot/blob/master/main.py) бот реализован через стейт машину [transitions](https://github.com/pytransitions/transitions). Именно этот файл работает на Heroku.


<h2>Задача</h2>
1. Бот должен поддерживать работу только с телеграммом - но вы должны учесть возможность подключения другого средства коммуникации (FB, VK, SKYPE);

2. Бот должен обрабатывать следующий диалог:    

    ⎯ Какую вы хотите пиццу? Большую или маленькую?

    ⎯ Большую

    ⎯ Как вы будете платить?

    ⎯ Наличкой

    ⎯ Вы хотите большую пиццу, оплата - наличкой?

    ⎯ Да

    ⎯ Спасибо за заказ

3. Для стейт машины необходимо использовать https://github.com/pytransitions/transitions;
4. Просьба добавить тесты для диалога;
5. Необходимо подключить его к телеграмму;
6. Код выложить на гитхаб или хероку.


<h2>Установка и развертывание</h2>
Зарегистрировать бота по [инструкции](https://core.telegram.org/bots).

Скопировать репозиторий

    $ git clone https://github.com/Ilia-Abrosimov/KVINT_Chat_Bot.git

В репозитории создать файл .env. В переменной TELEGRAM_TOKEN сохранить полученный при регистрации бота токен.

Установить виртуальное окружение для Windows / Mac или Linux

    $ python -m venv venv / python3 -m venv venv

Активировать виртуальное окружение для Windows / Mac или Linux

    $ source venv/Scripts/activate  / source venv/bin/activate 

Установить зависимости
    
    $ pip install requirements.txt

Запустить файл main.py

    $ python main.py