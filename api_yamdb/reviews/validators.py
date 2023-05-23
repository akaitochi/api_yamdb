import datetime as dt

from django.core.exceptions import ValidationError


def validate_year(value):
    if value > dt.today().year:
        raise ValidationError('Год выпуска не может быть больше текущего')
