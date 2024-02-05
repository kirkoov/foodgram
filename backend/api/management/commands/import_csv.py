"""This file is used to import a simple two-column ready-made csv collection
into a Postgre database for future use under the Foodgram project.

When in the folder containing the manage.py, run in your virtual env
`python manage.py import_csv` & you should be good to go on with the now
populated ingredients table.

"""
import csv

from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError, OperationalError

from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("\tImporting the ingredients csv...")
        try:
            with open("../data/ingredients.csv", newline="") as csvfile:
                reader = csv.reader(csvfile)
                Ingredient.objects.bulk_create(
                    Ingredient(
                        name=row[0],
                        measurement_unit=row[1],
                    )
                    for row in reader
                )

                self.stdout.write(
                    self.style.SUCCESS("<*>Data imported successfully<*>\n")
                )
        except IntegrityError as integ_err:
            print(f"<!>IntegrityError: {integ_err}<!>\n")
        except OperationalError as op_err:
            print(f"<!>OperationalError: {op_err}<!>\n")
        except CommandError as cmd_err:
            print(f"<!>CommandError: {cmd_err}<!>\n")
        except FileNotFoundError:
            print("<!>No csv file found<!>\n")
