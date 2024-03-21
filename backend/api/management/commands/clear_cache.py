"""This file is used to clear cache if needed. Run in your virtual env
`python manage.py clear cache`.

"""
from django.core.cache import cache
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        cache.clear()
        self.stdout.write("Cache cleared.\n")
