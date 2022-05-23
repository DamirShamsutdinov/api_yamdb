# from django.core.management import BaseCommand
# from reviews.models import Category
# import csv
# import os
# from api_yamdb.api_yamdb.settings import BASE_DIR
#
#
# def category_func():
#     with open('static/data/category.csv') as file:
#         reader = csv.reader(file)
#         next(reader)  # Advance past the header
#         Category.objects.all().delete()
#         for row in reader:
#             print(row)
#             Category.objects.create(
#                 id=row[0],
#                 name=row[1],
#                 slug=row[2],
#             ).save()
#
#
# class Command(BaseCommand):
#
#     def add_arguments(self, parser):
#         parser.add_argument('name_csv', type=str,)
#
#     def handle(self, *args, **options):
#         name_csv = options['name_csv']
#         path = os.path.join(BASE_DIR, f'static/data/{name_csv}.csv')
#         category_func(path)


import csv
import os
import sqlite3
from api_yamdb.api_yamdb.settings import BASE_DIR

con = sqlite3.connect("db.sqlite3")
cur = con.cursor()
filename = os.path.join(BASE_DIR, 'static/data/category.csv')
a_file = open(filename, 'r', encoding='utf-8')
rows = csv.reader(a_file)
cur.executemany("INSERT INTO reviews_category(id,name,slug)", rows)

cur.execute("SELECT * FROM db.sqlite3")
print(cur.fetchall())

con.commit()
con.close()