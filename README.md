# Продуктовый помощник

### Описание:
Сайт(и API), на котором пользователи могут публиковать рецепты, добавлять 
чужие рецепты в избранное и подписываться на публикации других авторов.
Сервис «Список покупок» позволит пользователям создавать список продуктов,
которые нужно купить для приготовления выбранных блюд.

### Стек технологий: 
Python 3, Django REST Framework, PostgreSQL, Gunicorn, Nginx, Яндекс.Облако(Ubuntu 20.04), GitHub Actions, Docker

### Как запустить проект на своем сервере:

Клонировать репозиторий(а можно только docker-compose.yml и nginx.conf, см. ниже):
```
git@github.com:noskov-sergey/foodgram-project-react.git
```
Залить на свой сервер файлы docker-compose.yml и nginx.conf(редачим под свой сервер), прямо в корень:
```
scp my_file username@host:<путь-на-сервере>
```

Прописываем секреты:
```
DOCKER_USERNAME=<логин для докера>
DOCKER_PASSWORD=<пароль>
HOST=<IP сервера>
USER=<пользователь на сервере>
SSH_KEY=<приватный ключ от компьтера, у которого есть доступ на сервер>
PASSPHRASE=<защитный пароль для ssh ключа, если есть>
TELEGRAM_TO=<Id бота в телегра, для отправки уведомления об успешном деплое>
TELEGRAM_TOKEN=<токен для бота>
DB_ENGINE=<django.db.backends.postgresql или любой другой>
DB_NAME=<postgres или любой другой>
POSTGRES_USER=<ваш пользователь>
POSTGRES_PASSWORD=<пароль для вашего пользователя>
DB_HOST=db
DB_PORT=5432
```

Запустить билд:
```
sudo docker-compose up -d
```
Запустить миграции, создать суперпользователя, собрать статику: 
```
sudo docker-compose exec api python manage.py migrate
sudo docker-compose exec api python manage.py createsuperuser
sudo docker-compose exec api python manage.py collectstatic --no-input
```
Заполнить БД тестовыми данными(ингредиенты и теги) :
``` 
sudo docker-compose exec api python manage.py import_db
```

Все, можно переходить сюда:
``` 
http://your.hostname:port(if needs)
``` 

### Автор проекта:
[Носков Сергей](https://github.com/noskov-sergey)

### Сервер:
Сервер доступен по адресу http://62.84.122.169/
