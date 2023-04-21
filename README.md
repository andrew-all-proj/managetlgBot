# tlg_short_video
Описание:
Бот предназначен для администрирования телеграмм каналов.
- добавления контента по времени
- удаление контента по времени
- хранение контента в БД
в будущем публикация старых постов  через определенное время

Установка приложения:
4. Копируем папку на сервер
5. обновляем sudo apt update
6. Запускаем ./install
7. переходим в папку с установленым приложением и активируем виртуальное окружение командой
    source venv/bin/activate

Установка базы данных PostgreSQL
1.Выполнить команду для скачивания и установки БД
    sudo apt -y install postgresql
2. Переходим под пользователя postgres
    sudo -i -u postgres
3. Создаем роль для БД (tlg_manager_bot)
    createuser --interactive
4. Создаем БД
    sudo -u postgres createdb tlg_manager_bot
5. Проверка 
 

    проверка соединения \conninfo
6. задать пароль 
    \password tlg_manager_bot (1)

Настройка приложения
1. Меняем пользователя sudo su tlg_manager_bot
2. Активируем виртуальное окружение source venv/bin/activate
3. Меняем настройки БД в файле nano config.py
4. Создание таблиц
   python sheme_db.py
5. Заполнить таблицу данными type_media
    python type_media/add_types_media.py
6. Добавить пользователя телеграмма
   python service/create_super_user.py
7. deactivate
8. 
    
   