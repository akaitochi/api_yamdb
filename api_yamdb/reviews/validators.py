from rest_framework import serializers


def validate_username(self, value):
    """Проверяем, что нельзя использовать 'me' в качестве username"""
    username = value.lower()
    if username == 'me':
        raise serializers.ValidationError(
            'Пользователя с username "me" нельзя создавать'
        )
