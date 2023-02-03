# yamdb_final
![workflow](https://github.com/DenisKtv/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

Проект YaMDb собирает отзывы пользователей на произведения. 

_Благодаря этому проекту можно:_
- оставлять к произведениям текстовые отзывы 
- ставить произведению оценку
- комментировать отзывы других пользователей
- получить список всех произведений, категорий, жанров, комментариев, отзывов

***
### Технологии

API Yatube использует open-source технологии:
- [Python 3.7 ](https://www.python.org/downloads/release/python-379/)
- [Django REST framework 3.12](https://www.django-rest-framework.org/community/3.12-announcement/)
- [Simple JWT-аутентификация с реализацией через код подтверждения](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
- [Posgres](https://www.postgresql.org/docs/)
- [Docker](https://www.postgresql.org/docs/)


## Шаблон заполнения .env в директории infra/ на примере еnv.example

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```


### Установка и запуск приложения в контейнерах

- Клонируйте проект
```
git clone [ссылка](https://github.com/DenisKtv/yamdb_final.git)
``` 

- Из папки 'infra/' соберем образ при помощи docker-compose

```
$ docker-compose up -d --build
```

- Выполняем миграции:

```
$ docker-compose exec web python manage.py migrate
```

- Создаем суперпользователя:

```
$ docker-compose exec web python manage.py createsuperuser
```

- Собираем статику:

```
$ docker-compose exec web python manage.py collectstatic --no-input
```

- В проекте есть дамп локальной базы, для заполнения базы выполните команду:

```
docker-compose exec web python manage.py loaddata fixtures.json
```

### Автор

Студент Я.Практикум - _Denis Kostiv_
