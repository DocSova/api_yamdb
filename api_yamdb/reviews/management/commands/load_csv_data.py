import csv
import os

from django.core.management import BaseCommand
from django.conf import settings
from django.db import IntegrityError

from reviews.models import (
    Category,
    Comment,
    Genre,
    GenreTitle,
    Review,
    Title
)
from users.models import User

FILES_CLASSES = {
    'category': Category,
    'genre': Genre,
    'titles': Title,
    'genre_title': GenreTitle,
    'users': User,
    'review': Review,
    'comments': Comment,
}

FIELDS = {
    'category': ('category', Category),
    'title_id': ('title', Title),
    'genre_id': ('genre', Genre),
    'author': ('author', User),
    'review_id': ('review', Review),
}

print_console = BaseCommand().stdout.write


def open_csv_file(file_name):
    """Менеджер контекста для открытия csv-файлов."""
    csv_file = file_name + '.csv'
    csv_path = os.path.join(settings.CSV_FILES_DIR, csv_file)
    try:
        with (open(csv_path, encoding='utf-8')) as file:
            return list(csv.reader(file))
    except FileNotFoundError:
        print_console(f'Файл {csv_file} не найден.')
        return


def change_foreign_values(data_csv):
    """Метод для изменения значений."""
    data_csv_copy = data_csv.copy()
    for field_key, field_value in data_csv.items():
        if field_key in FIELDS.keys():
            field_key0 = FIELDS[field_key][0]
            data_csv_copy[field_key0] = FIELDS[field_key][1].objects.get(
                pk=field_value)
    return data_csv_copy


def load_csv(file_name, class_name):
    """Осуществляет загрузку csv-файлов."""
    table_not_loaded = f'Таблица {class_name.__qualname__} не загружена.'
    table_loaded = f'Таблица {class_name.__qualname__} загружена.'
    data = open_csv_file(file_name)
    rows = data[1:]
    for row in rows:
        data_csv = dict(zip(data[0], row))
        data_csv = change_foreign_values(data_csv)
        try:
            table = class_name(**data_csv)
            table.save()
        except (ValueError, IntegrityError) as error:
            print_console(f'Ошибка в загружаемых данных. {error}. '
                          f'{table_not_loaded}')
            break
    print_console(table_loaded)


class Command(BaseCommand):
    """Класс загрузки тестовой базы данных."""

    def handle(self, *args, **options):
        for key, value in FILES_CLASSES.items():
            print_console(f'Загрузка таблицы {value.__qualname__}')
            load_csv(key, value)
