import json
from typing import List

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from backend.constants import (
    NUM_CHARS_INGREDIENT_NAME,
    NUM_CHARS_MEALTIME_HEX,
    NUM_CHARS_MEALTIME_NAME,
    NUM_CHARS_MEALTIME_SLUG,
    NUM_CHARS_MEASUREMENT_UNIT,
    TEST_NUM_INGREDIENTS,
    TEST_NUM_TAGS,
)
from .models import Ingredient, Recipe, Tag
from .validators import validate_hex_color, validate_slug_field

User = get_user_model()


class RecipeTests(APITestCase):
    prefix = "/api/"
    tags_url = f"{prefix}tags/"
    ingredients_url = f"{prefix}ingredients/"
    recipes_url = f"{prefix}recipes/"
    api_client = APIClient()
    test_tags: List[Tag] = []
    test_ingredients: List[Ingredient] = []
    test_recipes: List[Recipe] = []

    @classmethod
    def setUpTestData(cls):
        cls.create_test_user()

        for index in range(1, TEST_NUM_TAGS + 1):
            tag = Tag(
                name=f"Tag{index}",
                color=f"#E26C{index}D",
                slug=f"-{index}_",
            )
            cls.test_tags.append(tag)
        Tag.objects.bulk_create(cls.test_tags)

        for idx in range(1, TEST_NUM_INGREDIENTS + 1):
            ingredient = Ingredient(
                name=f"Ingredient{idx}",
                measurement_unit="g",
            )
            cls.test_ingredients.append(ingredient)
        Ingredient.objects.bulk_create(cls.test_ingredients)

        # for idx in range(1, TEST_NUM_RECIPES + 1):
        #     recipe = Recipe(
        #         ingredients=None,  # [{"id": 1123, "amount": 10}],
        #         tags=[1, random.randint(2, TEST_NUM_TAGS)],
        #         image="data:image/png;(base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9)fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
        #         name=f"TestRecipe{idx}",
        #         text=f"Cooking instructions for test recipe{idx} go here",
        #         cooking_time=random.randint(
        #             MIN_COOKING_TIME_MINS, MAX_COOKING_TIME_MINS
        #         ),
        #     )
        #     name=models.CharField(
        #         max_length=NUM_CHARS_RECIPE_NAME,
        #         verbose_name=_("recipe name"),
        #         help_text=_("Enter a name for your recipe"),
        #     )
        # image = models.ImageField(
        #     validators=[validate_img_size],
        #     upload_to="recipes/",
        #     verbose_name=_("recipe image"),
        #     help_text=_("Upload an image<=1MB for your recipe"),
        # )
        # text = models.TextField(
        #     verbose_name=_("recipe description"),
        #     help_text=_("Describe how to cook"),
        # )
        # cooking_time = models.PositiveSmallIntegerField(
        #     validators=[
        #         MinValueValidator(MIN_COOKING_TIME_MINS),
        #         MaxValueValidator(MAX_COOKING_TIME_MINS),
        #     ],
        #     verbose_name=_("cooking time"),
        #     help_text=_("Enter now many minutes it needs to cook"),
        # )
        # tags = models.ManyToManyField(
        #     Tag,
        #     verbose_name=_("mealtimes"),
        # )
        # author = models.ForeignKey(
        #     User,
        #     on_delete=models.CASCADE,
        #     related_name="recipes",
        #     verbose_name=_("author"),
        # )
        # ingredients = models.ManyToManyField(
        #     Ingredient,
        #     through=RecipeIngredient,
        #     verbose_name=_("ingredients"),
        # )
        #     cls.test_recipes.append(recipe)
        # Recipe.objects.bulk_create(cls.test_recipes)

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
        response = self.client.get(f"{self.ingredients_url}?name=Ingredient")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if TEST_NUM_INGREDIENTS == 2000:
            self.assertEqual(
                len(json.loads(response.content)), TEST_NUM_INGREDIENTS
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

    @staticmethod
    def test_create_same_ingredients():
        with pytest.raises(IntegrityError):
            Ingredient.objects.create(
                name="oh_same-ingredient",
                measurement_unit="kg",
            )
            Ingredient.objects.create(
                name="oh_same-ingredient",
                measurement_unit="kg",
            )

    # def test_recipe_page_available_anonymous_user(self):
    #     response = self.client.get(self.recipes_url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    @classmethod
    def create_test_user(cls):
        # "url": ,
        # "token_url": ,
        # "del_token_url": "/api/auth/token/logout/",
        # "set_pwd_url": "/api/users/set_password/",
        # "data": ,
        user_data = {
            "email": "standard@user.com",
            "username": "test_standard_uza",
            "first_name": "Test",
            "last_name": "Standard",
            "password": "wHat~Eva^_",
        }
        response = cls.api_client.post(
            "/api/users/",
            user_data,
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 1
        login_data = {
            "password": user_data["password"],
            "email": user_data["email"],
        }
        response = cls.api_client.post(
            "/api/auth/token/login/", login_data, format="json"
        )
        assert "auth_token" in json.loads(response.content)
        token = Token.objects.get(user__username=user_data["username"])
        cls.api_client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = cls.api_client.get("/api/users/me/")
        assert response.status_code == status.HTTP_200_OK
