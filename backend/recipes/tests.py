import pytest

from django.conf import settings
from django.db.utils import DataError
from django.test import TestCase

from .models import Tag


class RecipeTests(TestCase):
    def test_create_tag_name(self):
        with pytest.raises(DataError):
            Tag.objects.create(
                name=settings.NUM_CHARS_MEALTIME_NAME * "s" + "more",
                color=None,
                slug="",
            )

    def test_create_tag_color(self):
        with pytest.raises(DataError):
            Tag.objects.create(
                name=settings.NUM_CHARS_MEALTIME_NAME * "s",
                color="wrongHEX",
                slug=None,
            )
