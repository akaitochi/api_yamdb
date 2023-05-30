import csv

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import (Categories, Comment, Genres, Review, Titles, User)

DICT = {
    Categories: 'category.csv',
    Comment: 'comments.csv',
    Genres: 'genre.csv',
    Review: 'review.csv',
    Titles: 'titles.csv',
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
