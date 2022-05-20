import os

from api_yamdb.api_yamdb.settings import BASE_DIR
from django.core.management.base import BaseCommand

from api_yamdb.core.management.commands._models_parser_func import \
    category_parser, comments_parser, genre_parser, genre_title_parser, \
    review_parser, titles_parser, users_parser


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('name_csv', type=str, help='Название файла')

    def handle(self, *args, **options):
        name_csv = options['name_csv']
        path = os.path.join(BASE_DIR, f'static/data/{name_csv}.csv')

        parser_dict = {
            'users': users_parser,
            'category': category_parser,
            'genre': genre_parser,
            'titles': titles_parser,
            'genre_title': genre_title_parser,
            'review': review_parser,
            'comments': comments_parser,
        }

        parser_object = parser_dict[name_csv]
        parser_object(path)
