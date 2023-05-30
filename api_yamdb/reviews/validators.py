import datetime as dt

from django.core.exceptions import ValidationError

from rest_framework import serializers


def validate_year(value):
    if value > dt.date.today().year:
        raise ValidationError('Год выпуска не может быть больше текущего')


class ValidateUsername:
    """Валидатор имени пользователя"""

    def validate_username(self, value):
        """Проверяем, что нельзя использовать 'me' в качестве username"""
        username = value.lower()
        if username == 'me':
            raise serializers.ValidationError(
                'Пользователя с username "me" нельзя создавать'
            )
