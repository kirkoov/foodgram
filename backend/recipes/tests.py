import json
import random

import pytest
from api.views import IngredientViewSet, TagViewSet
from backend.constants import (
    NUM_CHARS_INGREDIENT_NAME,
    NUM_CHARS_MEALTIME_HEX,
    NUM_CHARS_MEALTIME_NAME,
    NUM_CHARS_MEALTIME_SLUG,
    NUM_CHARS_MEASUREMENT_UNIT,
)
from django.db.utils import DataError, IntegrityError
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from .models import Ingredient, Tag
from .validators import validate_hex_color, validate_slug_field


class RecipeTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = APIRequestFactory()
        cls.prefix = "/api/"

        cls.tags_url = f"{cls.prefix}tags/"
        cls.test_tags = []
        cls.request_tags = cls.factory.get(cls.tags_url)
        cls.view_tag_detail = TagViewSet.as_view({"get": "retrieve"})
        for index in range(random.randint(1, 10)):
            tag = Tag(
                name=f"Tag{index}",
                color=f"#E26C{index}D",
                slug=f"-{index}_",
            )
            cls.test_tags.append(tag)
        Tag.objects.bulk_create(cls.test_tags)
        cls.request_tag_detail = cls.factory.get(f"{cls.tags_url}/")

        cls.ingredients_url = f"{cls.prefix}ingredients/"
        cls.test_ingredients = []
        cls.request_ingredients = cls.factory.get(cls.ingredients_url)
        cls.view_ingredient_detail = IngredientViewSet.as_view(
            {"get": "retrieve"}
        )
        cls.test_ingredient_name = "Ingredient"
        for index in range(random.randint(1, 100)):
            ingredient = Ingredient(
                name=f"{cls.test_ingredient_name}{index}",
                measurement_unit="g",
            )
            cls.test_ingredients.append(ingredient)
        Ingredient.objects.bulk_create(cls.test_ingredients)
        cls.request_ingredient_detail = cls.factory.get(
            f"{cls.ingredients_url}/"
        )

        cls.recipes_url = f"{cls.prefix}recipes/"

    def test_get_taglist_200(self):
        response = TagViewSet.as_view({"get": "list"})(self.request_tags)
        if response.status_code != 200:
            raise DataError("Recipes: no 200 status code for tags.")

    def test_get_taglist_content(self):
        response = TagViewSet.as_view({"get": "list"})(self.request_tags)
        data = response.__dict__.get("data")
        if data is not None:
            tmp_slugs = []
            for new, test in zip(data, self.test_tags):
                self.assertEqual(new["name"], test.name)
                self.assertTrue(len(new["name"]) <= NUM_CHARS_MEALTIME_NAME)
                self.assertEqual(new["color"], test.color)
                self.assertTrue(len(new["color"]) <= NUM_CHARS_MEALTIME_HEX)
                self.assertIsNone(validate_hex_color(new["color"]))
                self.assertEqual(new["slug"], test.slug)
                self.assertTrue(len(new["slug"]) <= NUM_CHARS_MEALTIME_SLUG)
                self.assertIsNone(validate_slug_field(new["slug"]))
                tmp_slugs.append(new["slug"])
            # The slugs must be unique
            self.assertEqual(len(tmp_slugs), len(set(tmp_slugs)))
        else:
            raise DataError(
                "Recipes: errors in the test_get_taglist_content()."
            )

    def test_get_tagdetail_200_404(self):
        # In the test db, i.e. sqlite3, the tags start from 1
        if (then := len(self.test_tags) - 1) == 0:
            then = 1
        response = self.view_tag_detail(self.request_tag_detail, pk=then)
        if response.status_code != 200:
            raise DataError("Recipes: no 200 status code for tag details.")
        response = self.view_tag_detail(
            self.request_tag_detail, pk=len(self.test_tags) + 1
        )
        if response.status_code != 404:
            raise DataError("Recipes: no 404 status code for tag details.")

    def test_get_ingredientlist_200(self):
        response = IngredientViewSet.as_view({"get": "list"})(
            self.request_ingredients
        )
        if response.status_code != 200:
            raise DataError("Recipes: no 200 status code for ingredient list.")

    def test_get_ingedientlist_content(self):
        response = IngredientViewSet.as_view({"get": "list"})(
            self.request_ingredients
        )
        data = response.__dict__.get("data")
        if data is not None:
            data_sorted = sorted(data, key=lambda d: d["id"])
            for new, test in zip(data_sorted, self.test_ingredients):
                self.assertEqual(new["name"], test.name)
                self.assertTrue(len(new["name"]) <= NUM_CHARS_INGREDIENT_NAME)
                self.assertEqual(
                    new["measurement_unit"], test.measurement_unit
                )
                self.assertTrue(
                    len(new["measurement_unit"]) <= NUM_CHARS_MEASUREMENT_UNIT
                )
        else:
            raise DataError(
                "Recipes: errors in the test_get_ingedientlist_content()."
            )

    def test_ingredient_search(self):
        request = self.factory.get(
            f"{self.prefix}ingredients/?search={self.test_ingredient_name}"
        )
        response = IngredientViewSet.as_view({"get": "list"})(request)
        data = response.__dict__.get("data")
        self.assertEqual(len(data), len(self.test_ingredients))

    def test_create_same_ingredients_fails(self):
        with pytest.raises(IntegrityError):
            Ingredient.objects.create(
                name="The-same-ingredient",
                measurement_unit="kg",
            )
            Ingredient.objects.create(
                name="The-same-ingredient",
                measurement_unit="kg",
            )

    def test_get_ingredientdetail(self):
        response = self.view_ingredient_detail(
            self.request_ingredient_detail, pk=len(self.test_ingredients) - 1
        )
        if response.status_code != 200:
            raise DataError(
                "Recipes: no 200 status code for ingredient details."
            )
        response.render()
        self.assertEqual(
            json.loads(response.content),
            {
                "id": len(self.test_ingredients) - 1,
                "name": f"Ingredient{len(self.test_ingredients) - 2}",
                "measurement_unit": "g",
            },
        )

        response = self.view_ingredient_detail(
            self.request_ingredient_detail, pk=len(self.test_ingredients) + 1
        )
        if response.status_code != 404:
            raise DataError(
                "Recipes: no 404 status code for ingredient details."
            )
