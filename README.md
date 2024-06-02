# YaMDb

### Описание
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Список может быть расширен администратором.

Пользователи могут оставлять отзывы на произведения, оценивать их, оставлять отзывы и оставлять к отзывам комментарии. Из оценок формируется усреднённая оценка произведения — рейтинг. На одно произведение пользователь может оставить только один отзыв.

Добавлять отзывы, комментарии и ставить оценки могут только зарегистрированные пользователи.

Полная документация к API находится в файле `api_yamdb/static/redoc.yaml`.

### Используемые технологии
- Python 3.12
- Django
- DRF
- djangorestframework-simplejwt

### Как запустить проект
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/monk-time/api_yamdb.git
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
source env/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

### Пользовательские роли и права доступа

- Аноним — может просматривать описания произведений, читать отзывы и комментарии.
- Аутентифицированный пользователь (user) — может читать всё, как и Аноним, публиковать отзывы и ставить оценки произведениям, комментировать отзывы, редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Роль по умолчанию.
- Модератор (moderator) — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
- Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- Суперюзер Django - обладает правами Администратора.

### Ресурсы API:
- **auth**: аутентификация.
- **users**: пользователи.
- **titles**: произведения и информация о них.
- **categories**: категории произведений.
- **genres**: жанры произведений. Одно произведение может иметь несколько жанров
- **reviews**: отзывы на произведения. Каждый отзыв относится к определенному произведению.
- **comments**: комментарии к отзывам на произведения.

### Регистрация пользователя
1. Передайте на `/api/v1/auth/signup/` свои username и email. Использовать имя 'me' запрещено. Каждое поле должно быть уникальным. Если пользователя нет в базе данных, он будет создан.

```http
POST /api/v1/auth/signup/

{
    "email": "string",
    "username": "string"
}

```

2. На ваш email будет отправлен код подтверждения.
3. Передайте на `/api/v1/auth/token/` свой email и confirmation_code из письма, в ответе вы получите JWT-токен.

```http
POST /api/v1/auth/token/

{
    "username": "string",
    "confirmation_code": "string"
}
```

### Примеры работы с API

Получение списка всех категорий: `GET /api/v1/categories/`

Получение списка всех отзывов: `GET /api/v1/titles/{title_id}/reviews/`

Добавление жанра:

```http
POST /api/v1/genres/

{
    "name": "string",
    "slug": "string"
}
```

Добавление произведения:

```http
POST /api/v1/titles/

{
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": [
        "string"
    ],
    "category": "string"
}
```

Добавление пользователя:

```http
POST /api/v1/users/

{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
```

### Команда разработки
Глазков Никита [@DocSova](https://github.com/DocSova) (тимлид) - категории, жанры и произведения: модели, view и эндпойнты. Импорт данных в базу данных из .csv файлов.

Александр Донской [@donskoyaleksander](https://github.com/donskoyaleksander) (разработчик) - регистрация, подтверждение по e-mail, получение JWT-токена и управление пользователями. Права доступа.

Игорь Николаенко [@mrzoom007](https://github.com/mrzoom007) (разработчик) - отзывы и комментарии: модели, view и эндпойнты. Рейтинги произведений.