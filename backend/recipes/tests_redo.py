import json
import os
import random

# from pprint import pprint
from typing import List

# import pytest
from django.contrib.auth import get_user_model

# from django.db import IntegrityError
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from backend.constants import (  # PAGINATOR_NUM,; TEST_SERVER_URL,
    MAX_COOKING_TIME_MINS,
    MAX_INGREDIENT_AMOUNT,
    MIN_COOKING_TIME_MINS,
    MIN_INGREDIENT_AMOUNT,
    NUM_CHARS_INGREDIENT_NAME,
    NUM_CHARS_MEALTIME_HEX,
    NUM_CHARS_MEALTIME_NAME,
    NUM_CHARS_MEALTIME_SLUG,
    NUM_CHARS_MEASUREMENT_UNIT,
    NUM_CHARS_RECIPE_NAME,
    TEST_NUM_INGREDIENTS,
    TEST_NUM_RECIPES,
    TEST_NUM_TAGS,
)
from backend.settings import MEDIA_ROOT

from .models import Ingredient, Recipe, Tag
from .validators import validate_hex_color, validate_slug_field

User = get_user_model()


class RecipeTests(APITestCase):
    api_client = APIClient()
    another_api_client = APIClient()

    prefix = "/api/"
    tags_url = f"{prefix}tags/"
    users_url = f"{prefix}users/"
    ingredients_url = f"{prefix}ingredients/"
    recipes_url = f"{prefix}recipes/"
    token_url = f"{prefix}auth/token/"
    login_url = f"{token_url}login/"
    logout_url = f"{token_url}logout/"

    test_user1_data = {
        "email": "test_user1@example.com",
        "username": "test_user1",
        "first_name": "Test",
        "last_name": "User1",
        "password": "wHat~Eva^_",
    }
    test_user2_data = {
        "email": "test_user2@example.com",
        "username": "test_user2",
        "first_name": "Test",
        "last_name": "User2",
        "password": "wEva_$hWt",
    }

    test_tags: List[Tag] = []
    test_ingredients: List[Ingredient] = []
    test_recipes: List[Recipe] = []

    recipe_data = {
        "name": "TestMe recipe",
        "image": (
            "data:image/png;base64,"
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///"
            "9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggC"
            "ByxOyYQAAAABJRU5ErkJggg=="
        ),
        "cooking_time": MIN_COOKING_TIME_MINS,
        "text": "Instructions to cook go here.",
        "ingredients": [
            {
                "id": TEST_NUM_INGREDIENTS,
                "amount": MIN_INGREDIENT_AMOUNT,
            }
        ],
        "tags": [
            1,
        ],
        "is_favorited": False,
        "is_in_shopping_cart": False,
    }
    default_images = [
        "front-view-arrangement-healthy-breakfast-meal-with-yogurt.jpg",
        "vertical-shot-delicious-vegetable-meatballs-with-creamy-sauce.resized."
        "jpg",
        "korean-fish-cake-vegetable-soup-table.jpg",
        "lunch.resized.jpg",
        "dinner.resized.jpg",
        "two-tortillas.jpg",
        "breakfast.resized.jpg",
        "splashing-lemonade-with-mint-lemons-table-isolated-black.resized."
        "resized.jpg",
        "brunch.resized.jpg",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.create_test_users()
        cls.create_test_tags()
        cls.create_test_ingredients()
        cls.create_test_recipes_by_user1()

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
        tag_total = len(self.test_tags)
        self.assertTrue(tag_total >= 1)
        response = self.client.get(f"{self.tags_url}{tag_total}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tag = Tag.objects.get(id=tag_total)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": tag.id,
                "name": tag.name,
                "color": tag.color,
                "slug": tag.slug,
            },
        )
        response = self.client.get(
            f"{self.tags_url}{len(self.test_tags) + 1}/"
        )
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
            f"{self.ingredients_url}?name=find_me%20ing"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if TEST_NUM_INGREDIENTS == 2000:
            self.assertEqual(
                json.loads(response.content),
                [
                    {
                        "id": 2001,
                        "name": "find_me ingredient",
                        "measurement_unit": "shovel",
                    }
                ],
            )

    def test_ingredient_detail(self):
        ingredient_total = len(self.test_ingredients)
        self.assertTrue(ingredient_total >= 1)
        response = self.client.get(
            f"{self.ingredients_url}{ingredient_total}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ingredient = Ingredient.objects.get(id=ingredient_total)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": ingredient.id,
                "name": ingredient.name,
                "measurement_unit": ingredient.measurement_unit,
            },
        )

    # def test_list_recipes(self):
    #     recipe_total = Recipe.objects.count()
    #     if 1 < PAGINATOR_NUM < recipe_total:
    #         response = self.client.get(f"{self.recipes_url}?page=2")
    #         self.assertEqual(response.status_code, status.HTTP_200_OK)
    #         self.assertEqual(json.loads(response.content)["count"], recipe_total)
    #         self.assertEqual(
    #             json.loads(response.content)["next"],
    #             f"{TEST_SERVER_URL}{self.recipes_url}?page=3",
    #         )
    #         self.assertEqual(
    #             json.loads(response.content)["previous"],
    #             f"{TEST_SERVER_URL}{self.recipes_url}",
    #         )
    #         self.assertEqual(
    #             len(json.loads(response.content)["results"]),
    #             PAGINATOR_NUM,
    #         )
    #         for author_dict in json.loads(response.content)["results"]:
    #             self.assertEqual(
    #                 author_dict["author"]["email"],
    #                 self.test_user1_data["email"],
    #             )
    #
    #         response = self.client.get(f"{self.recipes_url}?limit=2")
    #         self.assertEqual(response.status_code, status.HTTP_200_OK)
    #         self.assertEqual(
    #             len(json.loads(response.content)["results"]),
    #             2,
    #         )
    #
    #         # response = self.client.get(f"{self.recipes_url}?is_favorited=1")
    #         # self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    #         # response = self.client.get(f"{self.recipes_url}?tags=dinner")
    #         # self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    #         response = self.client.get(f"{self.recipes_url}?author=1")
    #         self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    #         # tmp_tags = []
    #         # self.assertEqual(
    #         #     json.loads(response.content),
    #         #     [
    #         #         {
    #         #             "id": x.id,
    #         #             "name": x.name,
    #         #             "color": x.color,
    #         #             "slug": x.slug,
    #         #         }
    #         #         for x in Tag.objects.all()
    #         #     ],
    #         # )
    #     # for x in Tag.objects.all():
    #     #     self.assertTrue(len(x.name) <= NUM_CHARS_MEALTIME_NAME)
    #     #     self.assertTrue(len(x.color) <= NUM_CHARS_MEALTIME_HEX)
    #     #     self.assertIsNone(validate_hex_color(x.color))
    #     #     self.assertTrue(len(x.slug) <= NUM_CHARS_MEALTIME_SLUG)
    #     #     self.assertIsNone(validate_slug_field(x.slug))
    #     #     tmp_tags.append(x.slug)
    #     # self.assertEqual(Tag.objects.count(), len(set(tmp_tags)))

    # def test_create_recipe(self):
    #     recipe_count_ini = Recipe.objects.count()
    #     recipe_data = {
    #         "name": "Another recipe to add",
    #         "image": (
    #             "data:image/png;base64,"
    #             "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///"
    #             "9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggC"
    #             "ByxOyYQAAAABJRU5ErkJggg=="
    #         ),
    #         "cooking_time": 125,
    #         "text": "Instructions to cook another test recipe go here.",
    #         "ingredients": [
    #             {
    #                 "id": 1,
    #                 "amount": 11,
    #             },
    #             {
    #                 "id": 22,
    #                 "amount": 5,
    #             },
    #             {
    #                 "id": 333,
    #                 "amount": 10,
    #             },
    #         ],
    #         "tags": [2, 3],
    #     }
    #     # For the sake of this test, the temp images accumulated by now are
    #     # deleted.
    #     self.delete_tmp_images()
    #     self.log_in_and_tokenize_user()
    #     response = self.api_client.post(self.recipes_url, recipe_data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #
    #     self.assertEqual(Recipe.objects.count(), recipe_count_ini + 1)
    #     response = self.client.get(
    #         f"{self.recipes_url}{recipe_count_ini + 1}/", format="json"
    #     )
    #     tag_1 = Tag.objects.get(id=recipe_data["tags"][0])
    #     tag_2 = Tag.objects.get(id=recipe_data["tags"][1])
    #     first_test_user = User.objects.get(id=1)
    #     ingredient_1 = Ingredient.objects.get(id=recipe_data["ingredients"][0]["id"])
    #     ingredient_2 = Ingredient.objects.get(id=recipe_data["ingredients"][1]["id"])
    #     ingredient_3 = Ingredient.objects.get(id=recipe_data["ingredients"][2]["id"])
    #     img_path = f"{TEST_SERVER_URL}/media/recipes/"
    #     for image in os.listdir(MEDIA_ROOT / "recipes"):
    #         if image not in self.default_images:
    #             img_path += image
    #             break
    #     self.assertEqual(
    #         json.loads(response.content),
    #         {
    #             "id": recipe_count_ini + 1,
    #             "tags": [
    #                 {
    #                     "id": tag_1.id,
    #                     "name": tag_1.name,
    #                     "color": tag_1.color,
    #                     "slug": tag_1.slug,
    #                 },
    #                 {
    #                     "id": tag_2.id,
    #                     "name": tag_2.name,
    #                     "color": tag_2.color,
    #                     "slug": tag_2.slug,
    #                 },
    #             ],
    #             "author": {
    #                 "email": first_test_user.email,
    #                 "id": first_test_user.id,
    #                 "username": first_test_user.username,
    #                 "first_name": first_test_user.first_name,
    #                 "last_name": first_test_user.last_name,
    #                 "is_subscribed": False,
    #             },
    #             "ingredients": [
    #                 {
    #                     "id": recipe_data["ingredients"][0]["id"],
    #                     "name": ingredient_1.name,
    #                     "measurement_unit": ingredient_1.measurement_unit,
    #                     "amount": recipe_data["ingredients"][0]["amount"],
    #                 },
    #                 {
    #                     "id": recipe_data["ingredients"][1]["id"],
    #                     "name": ingredient_2.name,
    #                     "measurement_unit": ingredient_2.measurement_unit,
    #                     "amount": recipe_data["ingredients"][1]["amount"],
    #                 },
    #                 {
    #                     "id": recipe_data["ingredients"][2]["id"],
    #                     "name": ingredient_3.name,
    #                     "measurement_unit": ingredient_3.measurement_unit,
    #                     "amount": recipe_data["ingredients"][2]["amount"],
    #                 },
    #             ],
    #             "is_favorited": False,
    #             "is_in_shopping_cart": False,
    #             "name": recipe_data["name"],
    #             "image": img_path,
    #             "text": recipe_data["text"],
    #             "cooking_time": recipe_data["cooking_time"],
    #         },
    #     )
    #     recipe_count_ini += 1
    #     incomplete_data = self.recipe_data
    #     incomplete_data["name"] = None
    #     incomplete_data["image"] = None
    #
    #     response = self.api_client.post(
    #         self.recipes_url, incomplete_data, format="json"
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(Recipe.objects.count(), recipe_count_ini)
    #     response = self.client.post(self.recipes_url, self.recipe_data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #     self.assertEqual(Recipe.objects.count(), recipe_count_ini)
    #
    #     response = self.api_client.post(
    #         "a-wrong-url-somehow", incomplete_data, format="json"
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #     self.log_out_and_detokenize_user()
    #
    # def test_recipe_detail(self):
    #     # The json response structure is checked by the test_create_recipe(),
    #     # so there's no need to repeat the same here.
    #     id_ = Recipe.objects.count()
    #     self.assertTrue(id_ >= 1)
    #     readers = (self.client, self.api_client)
    #     for reader in readers:
    #         response = reader.get(f"{self.recipes_url}{id_}/")
    #         self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     id_ += 1
    #     response = self.client.get(f"{self.recipes_url}{id_}/")
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #
    # def test_recipe_patch(self):
    #     id_ = Recipe.objects.count()
    #     self.assertTrue(id_ >= 1)
    #     response = self.client.get(f"{self.recipes_url}{id_}/")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIn("image", json.loads(response.content))
    #     img_path = json.loads(response.content)["image"]  # Keep unchanged
    #     patch_data = {
    #         "ingredients": [
    #             {
    #                 "id": 4,
    #                 "amount": 4,
    #             },
    #             {
    #                 "id": 55,
    #                 "amount": 55,
    #             },
    #         ],
    #         "tags": [3],
    #         "name": "Fist user's recipe patched by the second user?",
    #         "text": "Patched cooking instructions now",
    #         "cooking_time": 1,
    #     }
    #     for patcher in (self.client, self.api_client):
    #         response = patcher.patch(
    #             f"{self.recipes_url}{id_}/", patch_data, format="json"
    #         )
    #         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #
    #     response = self.client.patch(
    #         f"where-did-you-get-this-url/{id_}/", patch_data, format="json"
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #
    #     self.log_in_and_tokenize_user()
    #     response = self.api_client.patch(
    #         f"{self.recipes_url}{id_}/", patch_data, format="json"
    #     )
    #     self.log_out_and_detokenize_user()
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     recipe = Recipe.objects.get(id=id_)
    #     user = User.objects.get(id=recipe.author.id)
    #
    #     tags = []
    #     for tag in patch_data["tags"]:
    #         t = Tag.objects.get(id=tag)
    #         tags.append({"id": t.id, "name": t.name, "color": t.color, "slug": t.slug})
    #     ingredients = []
    #     for ingredient in patch_data["ingredients"]:
    #         i = Ingredient.objects.get(id=ingredient["id"])
    #         ingredients.append(
    #             {
    #                 "amount": ingredient["amount"],
    #                 "id": ingredient["id"],
    #                 "measurement_unit": i.measurement_unit,
    #                 "name": i.name,
    #             }
    #         )
    #     self.assertEqual(
    #         json.loads(response.content),
    #         {
    #             "id": id_,
    #             "tags": tags,
    #             "author": {
    #                 "email": user.email,
    #                 "id": user.id,
    #                 "username": user.username,
    #                 "first_name": user.first_name,
    #                 "last_name": user.last_name,
    #                 "is_subscribed": False,
    #             },
    #             "ingredients": ingredients,
    #             "is_favorited": False,
    #             "is_in_shopping_cart": False,
    #             "name": patch_data["name"],
    #             "image": img_path,
    #             "text": patch_data["text"],
    #             "cooking_time": patch_data["cooking_time"],
    #         },
    #     )
    #     # 403
    # self.log_in_and_tokenize_another_user()
    # response = self.api_client.patch(
    #     f"{self.recipes_url}{id_}/", patch_data, format="json")
    # self.assertEqual(
    #     response.status_code,
    #     status.HTTP_403_FORBIDDEN,
    #     "Must be the 403 status code!",
    # )
    # self.log_out_and_detokenize_user()

    # self.log_in_and_tokenize_user()
    # patch_data["ingredients"] = None
    # patch_data["name"] = None
    # response = self.api_client.patch(
    #     f"{self.recipes_url}{id_}/", patch_data, format="json"
    # )
    # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # @staticmethod
    # def test_create_same_ingredients():
    #     with pytest.raises(IntegrityError):
    #         Ingredient.objects.create(
    #             name="oh_same-ingredient",
    #             measurement_unit="kg",
    #         )
    #         Ingredient.objects.create(
    #             name="oh_same-ingredient",
    #             measurement_unit="kg",
    #         )

    @classmethod
    def create_test_users(cls):
        response = cls.api_client.post(
            cls.users_url,
            cls.test_user1_data,
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        response = cls.another_api_client.post(
            cls.users_url,
            cls.test_user2_data,
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 2

    @classmethod
    def delete_tmp_images(cls):
        for image in os.listdir(MEDIA_ROOT / "recipes"):
            if image not in cls.default_images:
                os.remove(MEDIA_ROOT / "recipes" / image)

    @classmethod
    def create_test_tags(cls):
        for index in range(1, TEST_NUM_TAGS + 1):
            tag = Tag(
                name=f"Tag{index}",
                color=f"#E26C{index}D",
                slug=f"-{index}_",
            )
            cls.test_tags.append(tag)
        Tag.objects.bulk_create(cls.test_tags)
        assert Tag.objects.count() == TEST_NUM_TAGS

    @classmethod
    def create_test_ingredients(cls):
        for idx in range(1, TEST_NUM_INGREDIENTS + 1):
            ingredient = Ingredient(
                name=f"Ingredient{idx}",
                measurement_unit="g",
            )
            cls.test_ingredients.append(ingredient)
        Ingredient.objects.bulk_create(cls.test_ingredients)
        assert Ingredient.objects.count() == TEST_NUM_INGREDIENTS

    @classmethod
    def create_test_recipes_by_user1(cls):
        cls.log_in_and_tokenize_user()
        for idx in range(1, TEST_NUM_RECIPES + 1):
            cls.recipe_data["name"] = f"TestMe recipe {idx}"
            cls.recipe_data["cooking_time"] = random.randint(
                MIN_COOKING_TIME_MINS, MAX_COOKING_TIME_MINS
            )
            cls.recipe_data["text"] = random.randint(1, 5) * f"Cook test{idx}."
            cls.recipe_data["ingredients"] = [
                {
                    "id": random.randint(1, TEST_NUM_INGREDIENTS),
                    "amount": random.randint(
                        MIN_INGREDIENT_AMOUNT, MAX_INGREDIENT_AMOUNT
                    ),
                }
            ]
            cls.recipe_data["tags"] = [
                x for x in range(1, random.randint(2, TEST_NUM_TAGS))
            ]
            assert len(cls.recipe_data["ingredients"]) > 0
            assert len(cls.recipe_data["tags"]) > 0
            assert "data:image/png;base64," in cls.recipe_data["image"]
            assert len(cls.recipe_data["ingredients"]) <= NUM_CHARS_RECIPE_NAME
            assert len(cls.recipe_data["text"]) > 0
            assert cls.recipe_data["cooking_time"] >= MIN_COOKING_TIME_MINS
            response = cls.api_client.post(
                cls.recipes_url, cls.recipe_data, format="json"
            )
            assert response.status_code == status.HTTP_201_CREATED
        cls.log_out_and_detokenize_user()
        assert Recipe.objects.count() == TEST_NUM_RECIPES

    @classmethod
    def log_in_and_tokenize_user(cls):
        login_data = {
            "password": cls.test_user1_data["password"],
            "email": cls.test_user1_data["email"],
        }
        response = cls.api_client.post(
            cls.login_url, login_data, format="json"
        )
        assert "auth_token" in json.loads(response.content)
        token = Token.objects.get(
            user__username=cls.test_user1_data["username"]
        )
        cls.api_client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

    @classmethod
    def log_out_and_detokenize_user(cls):
        response = cls.api_client.post(cls.logout_url, format="json")
        cls.api_client.logout()
        assert response.status_code == status.HTTP_204_NO_CONTENT

    @staticmethod
    def delete_test_users():
        User.objects.all().delete()

    @classmethod
    def tearDownClass(cls):
        cls.api_client.logout()
        cls.delete_tmp_images()
        cls.delete_test_users()
