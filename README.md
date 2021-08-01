Название проекта - Foodgram 
Краткое описание - API для проекта Foodgram инстаграмм для еды(есть возможность создавать собственные рецепты, подписываться на авторов, добавлять в избранное, скачивать список покупок необходимых ингредиентов и.т.д), реализованное на основе REST_API framework. 
Создан алгоритм регистрации(по email) и аутентификации пользователей, добавлены пользовательские роли. 
Также реализованы запросы GET, POST, PATCH, DEL для получения или изменения данных в формате json. 
Сайт находится по адресу: http://84.201.156.189/ 
Доступ в админ панель: http://84.201.156.189/admin. Login admin@admin.com, пароль:admin 
Клонирование репозитория - git clone https://github.com/VladOS95-cyber/foodgram-project-react 
Инструкция по установке Docker(windows) - https://docs.docker.com/docker-for-windows/install/ 
Команда для создание суперпользователя - docker-compose exec web python manage.py createsuperuser 
Команда для заполнения базы начальными данными - ./manage.py loaddata fixtures.json 
Заполнение .env - проект использует базу данных PostgreSQL, и все переменные необходимые для настройки подключенияк базе, находятся в файле .env.

Автор проекта: Владислав Бронзов Почта автора: vladislav.bronzov@gmail.com
