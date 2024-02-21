from django_filters import (
    CharFilter,
    FilterSet,
    ModelMultipleChoiceFilter,
)
from django_filters.rest_framework.filters import BooleanFilter

from recipes.models import Ingredient, Recipe, Tag


class IngredientFilter(FilterSet):
    name = CharFilter(lookup_expr="startswith")

    class Meta:
        model = Ingredient
        fields = ("name",)


class RecipeFilter(FilterSet):
    tags = ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name="tags__slug",
        to_field_name="slug",
    )
    is_favorited = BooleanFilter(field_name="is_favorited")
    is_in_shopping_cart = BooleanFilter(field_name="is_in_shopping_cart")

    class Meta:
        model = Recipe
        fields = (
            "author",
            "tags",
            "is_favorited",
            "is_in_shopping_cart",
        )
