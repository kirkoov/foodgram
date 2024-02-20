# from rest_framework.filters import SearchFilter
from django_filters import CharFilter, FilterSet

from recipes.models import Ingredient


class IngredientFilter(FilterSet):
    name = CharFilter(lookup_expr="startswith")

    class Meta:
        model = Ingredient
        fields = ("name",)
