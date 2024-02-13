# import json
# import pytest
# from rest_framework.test import APIRequestFactory
# from sys import maxsize

# from django.conf import settings
# from django.core.exceptions import ValidationError
# from django.db.utils import DataError, IntegrityError
# from django.test import TestCase

# from .models import Ingredient, Tag
# from .validators import validate_hex_color, validate_slug_field
# from api.views import IngredientViewSet, TagViewSet


# class RecipeTests(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.factory = APIRequestFactory()

#         cls.test_ingredients = []
#         cls.test_name = "Ingredient"
#         for index in range(3):
#             ingredient = Ingredient(
#                 name=f"{cls.test_name}{index}",
#                 measurement_unit=settings.NUM_CHARS_MEASUREMENT_UNIT * "s",
#             )
#             cls.test_ingredients.append(ingredient)
#         Ingredient.objects.bulk_create(cls.test_ingredients)

#         cls.test_tags = []
#         cls.request_detail = cls.factory.get("/api/tags/0/")
#         cls.view_detail = TagViewSet.as_view({"get": "retrieve"})
#         for index in range(3):
#             tag = Tag(
#                 name=f"Tag {index}",
#                 color=f"#E26C{index}D",
#                 slug=f"-{index}_",
#             )
#             cls.test_tags.append(tag)
#         Tag.objects.bulk_create(cls.test_tags)

#     def test_create_tag_name(self):
#         with pytest.raises(DataError):
#             Tag.objects.create(
#                 name=settings.NUM_CHARS_MEALTIME_NAME * "s" + "more",
#                 color=None,
#                 slug=None,
#             )

#     def test_create_tag_color(self):
#         with pytest.raises(ValidationError):
#             Tag.objects.create(
#                 name=settings.NUM_CHARS_MEALTIME_NAME * "s",
#                 color=validate_hex_color("E26C2D"),
#                 slug=None,
#             )

#     def test_create_tag_slug(self):
#         Tag.objects.create(
#             name=settings.NUM_CHARS_MEALTIME_NAME * "s",
#             color=None,
#             slug=validate_slug_field("a-proper-slug"),
#         )

#     def test_get_taglist(self):
# request = self.factory.get("/api/tags/")
# view = TagViewSet.as_view({"get": "list"})
# response = view(request)
# data = response.__dict__.get("data")
# if data is not None:
#     for new, default in zip(data, self.test_tags):
#         assert new["name"] == default.name
#         assert new["color"] == default.color
#         assert new["slug"] == default.slug
# else:
#     raise DataError("No data in the test_get_taglist().")

#     def test_get_tagdetail(self):
#         response = self.view_detail(self.request_detail, pk=1)
#         data = response.__dict__.get("data")
#         if data is not None:  # 1 vs 0
#             assert data["name"] == self.test_tags[0].name
#             assert data["color"] == self.test_tags[0].color
#             assert data["slug"] == self.test_tags[0].slug
#         else:
#             raise DataError("No data in the test_get_tagdetail().")

#     def test_get_tagdetail_status200(self):
#         response = self.view_detail(self.request_detail, pk=1)
#         assert response.status_code == 200

#     def test_get_tagdetail_status404(self):
#         response = self.view_detail(self.request_detail, pk=maxsize)
#         assert response.status_code == 404

#     def test_create_valid_ingredient(self):
#         Ingredient.objects.create(
#             name=settings.NUM_CHARS_INGREDIENT_NAME,
#             measurement_unit=settings.NUM_CHARS_MEASUREMENT_UNIT * "s",
#         )

#     def test_create_same_ingredients(self):
#         with pytest.raises(IntegrityError):
#             Ingredient.objects.create(
#                 name=settings.NUM_CHARS_INGREDIENT_NAME,
#                 measurement_unit=settings.NUM_CHARS_MEASUREMENT_UNIT * "s",
#             )
#             Ingredient.objects.create(
#                 name=settings.NUM_CHARS_INGREDIENT_NAME,
#                 measurement_unit=settings.NUM_CHARS_MEASUREMENT_UNIT * "s",
#             )

#     def test_get_ingredientlist(self):
#         request = self.factory.get("/api/ingredients/")
#         view = IngredientViewSet.as_view({"get": "list"})
#         response = view(request)
#         data = response.__dict__.get("data")
#         if data is not None:
#             for new, default in zip(data, self.test_ingredients):
#                 assert new["name"] == default.name
#                 assert new["measurement_unit"] == default.measurement_unit
#         else:
#             raise DataError("No data in the test_get_ingredientlist().")

#     def test_get_ingredientdetail(self):
# request_detail = self.factory.get("/api/ingredients/2/")
# view_detail = IngredientViewSet.as_view({"get": "retrieve"})
# response = view_detail(request_detail, pk=2)
# response.render()
# self.assertEqual(
#     json.loads(response.content),
#     {
#         "id": 2,
#         "name": "Ingredient1",
#         "measurement_unit": settings.NUM_CHARS_MEASUREMENT_UNIT * "s",
#     },
# )

#     def test_ingredient_search(self):
#         request = self.factory.get(
#             f"/api/ingredients/?search={self.test_name}"
#         )
#         view = IngredientViewSet.as_view({"get": "list"})
#         response = view(request)
#         data = response.__dict__.get("data")
#         self.assertEqual(len(data), len(self.test_ingredients))
