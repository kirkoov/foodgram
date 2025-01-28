import django_filters
from django_filters import CharFilter, FilterSet, rest_framework
from recipes.models import Ingredient, Recipe


class IngredientFilter(FilterSet):
    name = CharFilter(lookup_expr="startswith")

    class Meta:
        model = Ingredient
        fields = ("name",)

# Changes for re-deployment sake


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.AllValuesMultipleFilter(
        field_name="tags__slug",
    )

    is_in_shopping_cart = django_filters.filters.NumberFilter(
        method="is_recipe_in_shoppingcart"
    )
    is_favorited = rest_framework.BooleanFilter(
        method="is_recipe_in_favorites"
    )

    def is_recipe_in_favorites(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(favorite__user_id=user.id)
        return queryset

    def is_recipe_in_shoppingcart(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(shoppingcart__user_id=user.id)
        return queryset

    class Meta:
        model = Recipe
        fields = (
            "author",
            "tags",
            "is_favorited",
            "is_in_shopping_cart",
        )
