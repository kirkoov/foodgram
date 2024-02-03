import pytest

from django.conf import settings
from django.db.utils import DataError
from django.test import TestCase

from .models import Tag


# @pytest.mark.parametrize("param", [param1, param2...])
# def test_function_that_throws_exception(param):
#     with pytest.raises(ValueError):
#        function_that_throws_exception(param)

# NUM_CHARS_MEALTIME_NAME = 200
# NUM_CHARS_MEALTIME_HEX = 7
# NUM_CHARS_MEALTIME_SLUG = 200


class RecipeTests(TestCase):
    # @pytest.mark.parametrize(
    #     "param",
    #     [settings.NUM_CHARS_MEALTIME_NAME * "s" + "more chars"],
    # )
    def test_create_tag(self):
        with pytest.raises(DataError):
            Tag.objects.create(
                name=settings.NUM_CHARS_MEALTIME_NAME * "s",
                color="#E26IDONTKNOWC2D",
                slug="breakfast",
            )

            # Tag.objects.create(
            #     name=settings.NUM_CHARS_MEALTIME_NAME * "s",
            #     color="-1",
            #     slug="breakfast",
            # )

        # color=settings.NUM_CHARS_MEALTIME_HEX * "123",
