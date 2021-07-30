Название проекта - Foodgram 
Краткое описание - API для проекта Foodgram инстаграмм для еды(есть возможность создавать собственные рецепты, подписываться на авторов, добавлять в избранное, скачивать список покупок необходимых ингредиентов и.т.д), реализованное на основе REST_API framework. 
Создан алгоритм регистрации(по email) и аутентификации пользователей, добавлены пользовательские роли. Также реализованы запросы GET, POST, PATCH, DEL для получения или изменения данных в формате json. 
Детальное описание запросов и получение данных находятся по адресу: http://127.0.0.1:8070/redoc/ 
Клонирование репозитория - git clone https://github.com/VladOS95-cyber/yamdb_final 
Инструкция по установке Docker(windows) - https://docs.docker.com/docker-for-windows/install/ 
Запуск контейнеров - docker start infra_sp2_db_1, docker start infra_sp2_nginx_1, infra_sp2_web_1 Запуск сервера - CMD python /code/manage.py runserver 0:8070 (прописать последней строкой в Dockerfile) 
Команда для создание суперпользователя - docker-compose exec web python manage.py createsuperuser 
Команда для заполнения базы начальными данными - ./manage.py loaddata fixtures.json 
Заполнение .env - проект использует базу данных PostgreSQL, и все переменные необходимые для настройки подключенияк базе, находятся в файле .env. 
Бейдж - https://github.com/VladOS95-cyber/yamdb_final/actions/workflows/yamdb_workflow.yaml/badge.svg

Автор проекта: Владислав Бронзов Почта автора: vladislav.bronzov@gmail.com
