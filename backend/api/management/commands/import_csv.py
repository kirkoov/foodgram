"""This file is used to import a simple two-column ready-made csv collection
into a Postgre database for future use under the Foodgram project.

When in the folder containing the manage.py, run in your virtual env
`python manage.py import_csv` & you should be good to go on with the now
populated ingredients table.

"""
import csv

from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError, OperationalError

# from reviews.models import (
#     Category,
#     Comment,
#     Genre,
#     Review,
#     Title,
# )  # GenreTitle
# from users.models import User


# def import_genres(rdr):
#     Genre.objects.bulk_create(
#         Genre(name=row["name"], slug=row["slug"]) for row in rdr
#     )


# def import_categories(rdr):
#     Category.objects.bulk_create(
#         Category(name=row["name"], slug=row["slug"]) for row in rdr
#     )


# def import_titles(rdr):
#     Title.objects.bulk_create(
#         Title(name=row["name"], year=row["year"], category_id=row["category"])
#         for row in rdr
#     )


# def import_users(rdr):
#     User.objects.bulk_create(
#         User(
#             id=int(row["id"]),
#             username=row["username"],
#             email=row["email"],
#             role=row["role"],
#             bio=row["bio"],
#             first_name=row["first_name"],
#             last_name=row["last_name"],
#         )
#         for row in rdr
#     )


# def import_genretitles(cont):
#     res = []
#     for line in cont:
#         try:
#             res.append([int(x) for x in line])
#         except ValueError as err:
#             print(f"<!>{err}<!>")

#     try:
#         connection = sqlite3.connect("db.sqlite3")
#         cursor = connection.cursor()
#         insert_records = """
# INSERT INTO reviews_title_genre (id, title_id, genre_id) VALUES (?, ?, ?)"""
#         cursor.executemany(insert_records, res)
#         connection.commit()
#         connection.close()
#     except sqlite3.Error as sq_err:
#         print(f"<!>{sq_err}<!>")


# def import_reviews(rdr):
#     Review.objects.bulk_create(
#         Review(
#             title_id=row["title_id"],
#             text=row["text"],
#             author_id=row["author"],
#             score=row["score"],
#             pub_date=row["pub_date"],
#         )
#         for row in rdr
#     )


# def import_comments(rdr):
#     Comment.objects.bulk_create(
#         Comment(
#             review_id=row["review_id"],
#             text=row["text"],
#             author_id=row["author"],
#             pub_date=row["pub_date"],
#         )
#         for row in rdr
#     )


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("\tImporting the ingredients csv...")
        try:
            with open("../data/ingredients.csv", "r") as f:
                # reader = csv.DictReader(f)
                csv.DictReader(f)
                self.stdout.write(
                    self.style.SUCCESS("<*>Data imported successfully<*>\n")
                )
        except IntegrityError as integ_err:
            print(
                f"<!>{integ_err}. Data 2 import in the DB already? Or"
                " unique values doubled?<!>\n"
            )
        except OperationalError as op_err:
            print(f"<!>{op_err}. DB is locked now or empty<!>\n")
        except CommandError as e:
            print(e)
        except FileNotFoundError:
            print("<!>No csv file found<!>\n")
