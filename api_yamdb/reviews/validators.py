from datetime import datetime

from django.core.exceptions import ValidationError


def validate_title_year(value):
    if value > int(datetime.now().year):
        msg = 'Значение года не может быть больше текущего'
        raise ValidationError(msg)
