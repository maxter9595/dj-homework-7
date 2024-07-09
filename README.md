# Алгоритм запуска проекта

1. Настройте виртуальное окружение и подключитесь к нему:
   - ``venv\Scripts\activate`` - для Windows
   - ``source venv/bin/activate`` - для MacOS и Linux
```bash
python -m venv venv
venv\Scripts\activate
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Убедитесь, что в settings.py правильно указаны параметры для подключения к базе данных (БД):
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'netology_classified_ads',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
    }
}
```

4. Создайте БД с именем, указанным в NAME (netology_classified_ads):
```bash
createdb -U postgres netology_classified_ads
```

5. Осуществите команды для создания миграций приложения с БД:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Заведите двух суперпользователей:
```bash
python manage.py createsuperuser
```

7. Запустите приложение:
```bash
python manage.py runserver
```

8. Войдите в административную панель (http://127.0.0.1:8000/admin/) и заведите простого пользователя через Users


9. Заведите токен для созданных пользователей через Tokens (административная панель). Примеры использования токенов представлены в ``requests-examples.http``


10. Откройте ``requests-examples.http`` в REST Client (VS Code) и реализуйте запросы


# Реализация запросов (на примере REST Client из VS Code)

- Примеры реализации запросов представлены в файле ``requests-examples.http``


- Создание объявления:
```http
@baseUrl = http://localhost:8000/api

###

# -- создвать объявление могут админы и пользователи
POST {{baseUrl}}/advertisements/
Content-Type: application/json
Authorization: Token 2c071f6b49703258910158cbe0699a8c2bdf4acf

{
  "title": "Шкаф IKEA",
  "description": "Срочно"
}
```


- Просмотр объявлений:
```http
# -- выводятся только объявления, имеющие статус OPEN и CLOSED
# -- объявления со статусом DRAFT может вывести только их автор (по токену)
GET {{baseUrl}}/advertisements/
Content-Type: application/json
```


- Получение объявлений с фильтрацией по дате:
```http
# получение объявлений с фильтрацией по дате (created_at_after)
GET {{baseUrl}}/advertisements/?created_at_after=2023-06-30
Content-Type: application/json

###

# получение объявлений с фильтрацией по дате (created_at_before)
GET {{baseUrl}}/advertisements/?created_at_before=2023-06-30
Content-Type: application/json
```


- Получение объявлений с фильтрацией по статусу:
```http
# -- выводятся только объявления, имеющие статус OPEN и CLOSED
GET {{baseUrl}}/advertisements/?status=OPEN
Content-Type: application/json
```


- Получение объявлений с фильтрацией по создателю:
```http
GET {{baseUrl}}/advertisements/?creator=1
Content-Type: application/json
```


- Обновление объявления:
```http
# -- админы могут менять любые объявления
# -- пользователи могут менять только свое объявление
# -- /int/ - id объявления
PATCH  {{baseUrl}}/advertisements/1/
Content-Type: application/json
Authorization: Token 2c071f6b49703258910158cbe0699a8c2bdf4acf

{
  "status": "OPEN"
}
```


- Получение объявлений из DRAFT (в обычном GET-запросе их нет):
```http
# -- объявление показывается только его автору (по токену)
GET {{baseUrl}}/advertisements/?status=DRAFT
Content-Type: application/json
Authorization: Token 2c071f6b49703258910158cbe0699a8c2bdf4acf
```


- Добавление объявления в избранные:
```http
# -- автор объявления не может добавить своё объявление в избранные
# -- /int/ - id объявления
POST {{baseUrl}}/advertisements/1/add_to_favorites/
Content-Type: application/json
Authorization: Token 8ae9ac82428229f90221b137bedcc56e46485b38
```


- Получение списка всех собственных избранных объявлений:
```http
## -- выводит все объявления, которые автор добавил в избранные
GET {{baseUrl}}/advertisements/favorite_advertisements/
Content-Type: application/json
Authorization: Token 8ae9ac82428229f90221b137bedcc56e46485b38
```


- Получение списка избранных объявлений по фильтрации:
```http
## -- фильтрация аналогична случаю {{baseUrl}}/advertisements/
GET {{baseUrl}}/advertisements/favorite_advertisements/?created_at_after=2023-06-30
Content-Type: application/json
Authorization: Token 8ae9ac82428229f90221b137bedcc56e46485b38
```


- Удаление объявления из избранных:
```http
## -- удаляется только у автора избранного объявления
# -- /int/ - id объявления
DELETE {{baseUrl}}/advertisements/1/remove_from_favorites/
Content-Type: application/json
Authorization: Token 8ae9ac82428229f90221b137bedcc56e46485b38
```


- Удаление объявления:
```http
# -- админы могут удалять любые объявления
# -- пользователи могут удалять только свои объявления
# -- /int/ - id объявления
DELETE  {{baseUrl}}/advertisements/1/
Content-Type: application/json
Authorization: Token 2c071f6b49703258910158cbe0699a8c2bdf4acf
```


# Текст задания ("Backend для приложения с объявлениями")

## Описание

Необходимо реализовать бэкенд для мобильного приложения с объявлениями. Объявления можно создавать и просматривать. Есть возможность фильтровать объявления по дате и статусу.

Создавать могут только авторизованные пользователи. Для просмотра объявлений авторизация не нужна.

У объявления есть статусы: `OPEN`, `CLOSED`. Необходимо валидировать, что у пользователя не больше 10 открытых объявлений.

Обновлять и удалять объявление может только его автор.

Чтобы боты и злоумышленники не нагружали нашу систему, добавьте лимиты на запросы:

- для неавторизованных пользователей: 10 запросов в минуту;
- для авторизованных пользователей: 20 запросов в минуту.

## Реализация

- Используйте `DateFromToRangeFilter` для фильтрации по дате https://django-filter.readthedocs.io/en/stable/ref/filters.html#datefromtorangefilter.

Пример работы:
![Фильтрация по дате](./screenshots/date_filter.png)

- В настройках подключено приложение `rest_framework.authtoken` и сконфигурирован `DEFAULT_AUTHENTICATION_CLASSES`. Для того, чтобы завести токен для пользователя, проделайте следующие шаги:

  - создайте пользователя через админку,
  - также через админку заведите ему токен,
  - этот токен используйте в запросах, передавая его в заголовках.

- Так как интерфейс BrowserableAPI в DRF не позволяет передавать заголовки с токеном, используйте Postman или HTTP-клиент VSCode.

Примеры:

Успешный запрос:
![Успех](./screenshots/success.png)

Неправильный токен:
![Неправильный токен](./screenshots/bad_token.png)

- Для переопределения доступов для отдельных методов `ViewSet` используется метод `get_permissions`. Он добавлен в заготовку, следует с ним ознакомиться и посмотреть с помощью breakpoint'ов в какой момент DRF его вызывает.

- Валидацию удаления чужого объявления следует делать:

  - либо внутри метода `destroy` https://www.django-rest-framework.org/api-guide/viewsets/#viewset-actions — это чуть проще;
  - либо определяя дополнительный класс-наследник `BasePermission`, дополнительно добавляя его в список `get_permissions` https://www.django-rest-framework.org/api-guide/permissions/#examples — это правильнее, и этот класс можно переиспользовать для других методов.

    Любой вариант допустим в рамках этого задания.

- С примерами запросов к API вы можете ознакомиться в [файле requests-examples.http](./requests-examples.http).

# Важно

Приложение называется `advertisements`, такие слова являются триггерами для блокировщиков рекламы (например, uBlock Origin). Рекомендуется отключить блокировщик, если вы им пользуетесь, либо переименовать приложение.

## Подсказки

1. В места, где нужно добавлять код, включены `TODO`-комментарии.

2. Ознакомьтесь целиком со структурой проекта. Разберите, как работает код в заготовке, например, проставляется поле создателя объявления таким образом, чтобы злоумышленник не мог создавать объявления от чужого лица.

3. Используйте возможность указывать `fields` в `Meta` внутри `FilterSet` класса, чтобы не задавать фильтры, которые могут сгенерироваться автоматически.

4. Админка Джанго по умолчанию даст возможность создания и редактирования пользователей и токенов. Этим удобно пользоваться для локального создания сущностей.

## Дополнительные задания (не обязательные к выполнению)

### Права для админов

- Реализуйте функциональность для админов. Админы могут менять и удалять любые объявления.

### Избранные объявления

- Добавить возможность добавлять объявления в избранное. Автор объявления не может добавить своё объявление в избранное. Должна быть возможность фильтрации по избранным объявлениям. Например, пользователь хочет посмотреть все объявления, которые он добавил в избранное.

- Для того, чтобы добавить дополнительный метод с урлом во ViewSet, вам может пригодиться декоратор `action` из `DRF`.

### Добавить статус `DRAFT`

- Добавьте статус `DRAFT` — черновик. Пока объявление в черновике, оно показывается только автору объявления, другим пользователям оно недоступно.

## Документация по проекту

Для запуска проекта необходимо

Установить зависимости:

```bash
pip install -r requirements.txt
```

Вам необходимо будет создать базу в postgres и прогнать миграции:

```base
manage.py migrate
```

Выполнить команду:

```bash
python manage.py runserver
```
