import csv

from django.core.management import BaseCommand
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = "Loads data from csv-files"

    def handle(self, *args, **options):

        print("Loading User data")
        with open('static/data/users.csv', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            n = 0
            for row in reader:
                User(
                    id=row[0],
                    username=row[1],
                    email=row[2],
                    role=row[3],
                    bio=row[4],
                    first_name=row[5],
                    last_name=row[6],
                ).save()
                n += 1
                print(f'done {n}')

        print("Loading Category data")
        with open('static/data/category.csv', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            n = 0
            for row in reader:
                Category(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                ).save()
                n += 1
                print(f'done {n}')

        print("Loading Genre data")
        with open('static/data/genre.csv', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            n = 0
            for row in reader:
                Genre(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                ).save()
                n += 1
                print(f'done {n}')

        print("Loading Title data")
        with open('static/data/titles.csv', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            n = 0
            for row in reader:
                category = Category.objects.get(id=row[3])
                Title(
                    id=row[0],
                    name=row[1],
                    year=row[2],
                    category=category
                ).save()
                n += 1
                print(f'done {n}')

        print("Loading GenreTitle data")
        with open('static/data/genre_title.csv', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            n = 0
            for row in reader:
                title_id = Title.objects.get(id=row[1])
                genre_id = Genre.objects.get(id=row[2])
                GenreTitle(
                    id=row[0],
                    title=title_id,
                    genre=genre_id
                ).save()
                n += 1
                print(f'done {n}')

        print("Loading Reviews data")
        with open('static/data/review.csv', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            n = 0
            for row in reader:
                title = Title.objects.get(id=row[1])
                author = User.objects.get(id=row[3])
                Review(
                    id=row[0],
                    title_id=title.id,
                    text=row[2],
                    author=author,
                    score=row[4],
                    pub_date=row[5],
                ).save()
                n += 1
                print(f'done {n}')

    print("Loading Comment data")
    with open('static/data/comments.csv', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        n = 0
        for row in reader:
            review_id = Review.objects.get(id=row[1])
            author = User.objects.get(id=row[3])
            Comment.objects.create(
                id=row[0],
                review=review_id,
                text=row[2],
                author=author,
                pub_date=row[4]
            ).save()
            n += 1
            print(f'done {n}')
