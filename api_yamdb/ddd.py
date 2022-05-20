import csv

from django.db.backends import sqlite3

con = sqlite3.connect("db.sqlite3")
cur = con.cursor()

a_file = open("test.csv")
rows = csv.reader(a_file)
cur.executemany("INSERT INTO data VALUES (?, ?)", rows)

cur.execute("SELECT * FROM data")
print(cur.fetchall())

con.commit()
con.close()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('name_csv', type=str, help='Название файла')

    def handle(self, *args, **options):
        name_csv = options['name_csv']