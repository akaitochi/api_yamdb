import csv

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import (Category, Genre, Title, User)


DICT = {
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    User: 'users.csv',
}


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for model, base in DICT.items():
            with open(
                f'{settings.BASE_DIR}/static/data/{base}',
                'r', encoding='utf-8'
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                model.objects.bulk_create(model(**data) for data in reader)

        self.stdout.write(self.style.SUCCESS('Данные успешно загружены'))
