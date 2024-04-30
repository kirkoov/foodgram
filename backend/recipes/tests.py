import json

# import random
# from pprint import pprint as pp
from typing import List

# import pytest
from django.contrib.auth import get_user_model

# from django.db.utils import DataError, IntegrityError
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, APITestCase

# from api.views import IngredientViewSet, RecipeViewSet, TagViewSet
from backend.constants import (
    NUM_CHARS_INGREDIENT_NAME,
    NUM_CHARS_MEALTIME_HEX,
    NUM_CHARS_MEALTIME_NAME,
    NUM_CHARS_MEALTIME_SLUG,
    NUM_CHARS_MEASUREMENT_UNIT,
    TEST_NUM_INGREDIENTS,
    TEST_NUM_TAGS,
)
from .models import Ingredient, Tag
from .validators import validate_hex_color, validate_slug_field

User = get_user_model()


class RecipeTests(APITestCase):
    prefix = "/api/"
    tags_url = f"{prefix}tags/"
    ingredients_url = f"{prefix}ingredients/"
    recipes_url = f"{prefix}recipes/"
    api_client = APIClient()
    factory = APIRequestFactory()
    test_tags: List[Tag] = []
    test_ingredients: List[Ingredient] = []

    @classmethod
    def setUpTestData(cls):
        for index in range(1, TEST_NUM_TAGS + 1):
            tag = Tag(
                name=f"Tag{index}",
                color=f"#E26C{index}D",
                slug=f"-{index}_",
            )
            cls.test_tags.append(tag)
        Tag.objects.bulk_create(cls.test_tags)

        for idx in range(1, TEST_NUM_INGREDIENTS):
            ingredient = Ingredient(
                name=f"Ingredient{idx}",
                measurement_unit="g",
            )
            cls.test_ingredients.append(ingredient)
        Ingredient.objects.bulk_create(cls.test_ingredients)

        # cls.test_recipes = []
        # cls.request_recipes = cls.factory.get(cls.recipes_url)
        # cls.view_recipe_detail = RecipeViewSet.as_view({"get": "retrieve"})
        # cls.test_recipe_name = "Test recipe"
        # cls.request_recipe_detail = cls.factory.get(f"{cls.recipes_url}/")

    def test_list_tags(self):
        response = self.client.get(self.tags_url)
        tmp_tags = []
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            [
                {
                    "id": x.id,
                    "name": x.name,
                    "color": x.color,
                    "slug": x.slug,
                }
                for x in Tag.objects.all()
            ],
        )
        for x in Tag.objects.all():
            self.assertTrue(len(x.name) <= NUM_CHARS_MEALTIME_NAME)
            self.assertTrue(len(x.color) <= NUM_CHARS_MEALTIME_HEX)
            self.assertIsNone(validate_hex_color(x.color))
            self.assertTrue(len(x.slug) <= NUM_CHARS_MEALTIME_SLUG)
            self.assertIsNone(validate_slug_field(x.slug))
            tmp_tags.append(x.slug)
        self.assertEqual(Tag.objects.count(), len(set(tmp_tags)))

    def test_tag_detail(self):
        id_ = len(self.test_tags)
        self.assertTrue(id_ >= 1)
        response = self.api_client.get(f"{self.tags_url}{id_}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tag = Tag.objects.get(id=id_)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": tag.id,
                "name": tag.name,
                "color": tag.color,
                "slug": tag.slug,
            },
        )
        id_ = len(self.test_tags) + 1
        response = self.api_client.get(f"{self.tags_url}{id_}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_ingredients(self):
        response = self.client.get(self.ingredients_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tmp_ingredients = []
        self.assertEqual(
            json.loads(response.content),
            [
                {
                    "id": x.id,
                    "name": x.name,
                    "measurement_unit": x.measurement_unit,
                }
                for x in Ingredient.objects.all()
            ],
        )
        for x in Ingredient.objects.all():
            self.assertTrue(len(x.name) <= NUM_CHARS_INGREDIENT_NAME)
            self.assertTrue(
                len(x.measurement_unit) <= NUM_CHARS_MEASUREMENT_UNIT
            )
            tmp_ingredients.append(x.name)
        self.assertEqual(Ingredient.objects.count(), len(set(tmp_ingredients)))

    def test_ingredient_search(self):
        count_ini = Ingredient.objects.count()
        Ingredient.objects.create(
            name="find_me ingredient",
            measurement_unit="shovel",
        )
        self.assertEqual(Ingredient.objects.count(), count_ini + 1)
        response = self.client.get(
            f"{self.ingredients_url}?name=find_me%20ingredient"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if TEST_NUM_INGREDIENTS == 1000:
            self.assertEqual(
                json.loads(response.content),
                [
                    {
                        "id": 1000,
                        "name": "find_me ingredient",
                        "measurement_unit": "shovel",
                    }
                ],
            )
        response = self.client.get(f"{self.ingredients_url}?name=Ingredient")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if TEST_NUM_INGREDIENTS == 1000:
            self.assertEqual(
                len(json.loads(response.content)), TEST_NUM_INGREDIENTS - 1
            )

    def test_ingredient_detail(self):
        id_ = len(self.test_ingredients)
        self.assertTrue(id_ >= 1)
        response = self.api_client.get(f"{self.ingredients_url}{id_}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ingredient = Ingredient.objects.get(id=id_)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": ingredient.id,
                "name": ingredient.name,
                "measurement_unit": ingredient.measurement_unit,
            },
        )

    # @staticmethod
    # def test_create_same_ingredients_fails():
    #     with pytest.raises(IntegrityError):
    #         Ingredient.objects.create(
    #             name="The-same-ingredient",
    #             measurement_unit="kg",
    #         )
    #         Ingredient.objects.create(
    #             name="The-same-ingredient",
    #             measurement_unit="kg",
    #         )
    #
    # def test_get_ingredient_detail(self):
    #     id_ = 1
    #     request_detail = self.factory.get(
    #         f"http://testserver/api/ingredients/{id_}/"
    #     )
    #     response = self.view_ingredient_detail(request_detail, pk=id_)
    #     if response.render():
    #         self.assertEqual(
    #             json.loads(response.content),
    #             {
    #                 "id": id_,
    #                 "name": f"Ingredient{id_ - 1}",
    #                 "measurement_unit": "g",
    #             },
    #         )
    #     else:
    #         raise DataError(
    #             "Recipes: no rendered content from the "
    #             "test_get_ingredient_detail()."
    #         )
    #
    # def test_recipe_page_available_anonymous_user(self):
    #     response = self.client.get(self.recipes_url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
