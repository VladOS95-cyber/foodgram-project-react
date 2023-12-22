## Foodgram App

## Description
The Foodgram project is a service for publishing culinary recipes.

Demo site: http://84.201.156.189

Admin panel: http://http://84.201.156.189/admin

User registration.

Create, Modify, Delete recipes.

Add recipes to favorites and browse all favorites.

Filter recipes by tags.

Subscribe to authors and view recipes by a specific author.

Adding recipes and creating a shopping list for their preparation.

## Installation 

To work with the project, you need to install Docker: https://docs.docker.com/engine/install/

Clone the repository to your server with the command:

https://github.com/VladOS95-cyber/foodgram-project-react
Go to the project gurney:

cd foodgram-project-react
Create an environment file

touch .env
And fill it in:

POSTGRES_NAME = postgres # postgres database name
POSTGRES_USER = postgres # postgres username
POSTGRES_PASSWORD = postgres # password for postgres database
DB_HOST = postgresql # database hostname
DB_PORT = 5432 # port

Go to the infra directory and start creating containers:
```bash
docker-compose up -d --build
```

Initial project setup:
```bash
docker-compose exec backend python manage.py migrate --noinput
```
```bash
docker-compose exec backend python manage.py collectstatic --no-input
```
Create superuser:
```bash
docker-compose exec backend python manage.py createsuperuser
```

Loading fixtures
```bash
docker exec -it backend python manage.py loaddata fixtures.json
```
Once built, the project will be accessible by the hostname of your machine where the project was deployed.

Project author: Vladislav Bronzov, mail: vladislav.bronzov@gmail.com
