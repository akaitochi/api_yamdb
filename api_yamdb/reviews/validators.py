import datetime as dt
import re

from django.core.exceptions import ValidationError

# from .models import User


def validate_year(value):
    if value > dt.date.today().year:
        raise ValidationError('Год выпуска не может быть больше текущего')


class ValidateUsername:
    """Валидатор имени пользователя."""

    def validate_username(self, value):
        """Проверяем, что нельзя использовать 'me' в качестве username."""
        if value.lower() == 'me':
            raise ValidationError(
                'Пользователя с username "me" нельзя создавать'
            )
        if not re.match(r"^[\w.@+-]+\Z", value):
            raise ValidationError(
                'username содержит недопустимые символы'
            )
        return value


# class ValidateEmail:
#     """Валидатор адреса электронной почты"""

    # def validate_email(self, value):
    #     if User.objects.filter(email=value.lower()).exists():
    #         raise ValidationError(
    #             'Почта уже используется'
    #         )
