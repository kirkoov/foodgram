import pytest

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.utils import DataError
from django.test import TestCase

from .models import Tag
from .validators import validate_hex_color, validate_slug_field


class RecipeTests(TestCase):
    def test_create_tag_name(self):
        with pytest.raises(DataError):
            Tag.objects.create(
                name=settings.NUM_CHARS_MEALTIME_NAME * "s" + "more",
                color=None,
                slug="",
            )

    def test_create_tag_color(self):
        with pytest.raises(ValidationError):
            Tag.objects.create(
                name=settings.NUM_CHARS_MEALTIME_NAME * "s",
                color=validate_hex_color("E26C2D"),
                slug=None,
            )

    def test_create_tag_slug(self):
        Tag.objects.create(
            name=settings.NUM_CHARS_MEALTIME_NAME * "s",
            color="",
            slug=validate_slug_field("a-proper-slug"),
        )
