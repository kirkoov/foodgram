import json
import random

import pytest
from django.db.utils import DataError, IntegrityError
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APIRequestFactory, APITestCase

from api.views import IngredientViewSet, TagViewSet
from backend.constants import (
    NUM_CHARS_INGREDIENT_NAME,
    NUM_CHARS_MEALTIME_HEX,
    NUM_CHARS_MEALTIME_NAME,
    NUM_CHARS_MEALTIME_SLUG,
    NUM_CHARS_MEASUREMENT_UNIT,
)
from .models import Ingredient, Tag
from .validators import validate_hex_color, validate_slug_field


class RecipeTests(APITestCase):
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
        cls.view_ingredient_detail = IngredientViewSet.as_view({"get": "retrieve"})
        cls.test_ingredient_name = "Ingredient"
        for index in range(random.randint(1, 100)):
            ingredient = Ingredient(
                name=f"{cls.test_ingredient_name}{index}",
                measurement_unit="g",
            )
            cls.test_ingredients.append(ingredient)
        Ingredient.objects.bulk_create(cls.test_ingredients)
        cls.request_ingredient_detail = cls.factory.get(f"{cls.ingredients_url}/")

        cls.recipes_url = f"{cls.prefix}recipes/"

    def test_get_taglist_200(self):
        response = self.client.get(self.tags_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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
            raise DataError("Recipes: errors in the test_get_taglist_content().")

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
        response = self.client.get(self.ingredients_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_ingedientlist_content(self):
        response = IngredientViewSet.as_view({"get": "list"})(self.request_ingredients)
        data = response.__dict__.get("data")
        if data is not None:
            data_sorted = sorted(data, key=lambda d: d["id"])
            for new, test in zip(data_sorted, self.test_ingredients):
                self.assertEqual(new["name"], test.name)
                self.assertTrue(len(new["name"]) <= NUM_CHARS_INGREDIENT_NAME)
                self.assertEqual(new["measurement_unit"], test.measurement_unit)
                self.assertTrue(
                    len(new["measurement_unit"]) <= NUM_CHARS_MEASUREMENT_UNIT
                )
        else:
            raise DataError("Recipes: errors in the test_get_ingedientlist_content().")

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
        id_ = 1
        request_detail = self.factory.get(f"http://testserver/api/ingredients/{id_}/")
        response = self.view_ingredient_detail(request_detail, pk=id_)
        if response.render():
            self.assertEqual(
                json.loads(response.content),
                {
                    "id": id_,
                    "name": f"Ingredient{id_ - 1}",
                    "measurement_unit": "g",
                },
            )
        else:
            raise DataError(
                "Recipes: no rendered content from the test_get_ingredientdetail()."
            )

    def test_recipe_page_available_anonymous_user(self):
        response = self.client.get(self.recipes_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @pytest.fixture(autouse=True, scope="class")
    def _test_recipe_page_available_signed_user(self, get_standard_user_data):
        self._test_recipe_page_available_signed_user = get_standard_user_data
        client = APIClient()
        response = client.post(
            self._test_recipe_page_available_signed_user["url"],
            self._test_recipe_page_available_signed_user["data"],
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        test_data = {
            "password": self._test_recipe_page_available_signed_user["data"][
                "password"
            ],
            "email": self._test_recipe_page_available_signed_user["data"]["email"],
        }
        response = client.post(
            self._test_recipe_page_available_signed_user["token_url"],
            test_data,
            format="json",
        )
        token = Token.objects.get(
            user__username=self._test_recipe_page_available_signed_user["data"][
                "username"
            ]
        )
        client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = client.get(self.recipes_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.__dict__)
        client.logout()

    # def test_recipe_create(self):
    #     data = (
    #         {
    #             "ingredients": [
    #                 {"id": len(self.test_ingredients) - 1, "amount": self.test_ingredients[]}
    #             ],
    #             "tags": [1, 2],
    #             "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
    #             "name": "Test recipe name",
    #             "text": "Cooking instructions for the test recipe name",
    #             "cooking_time": 1,
    #         },
    #     )
