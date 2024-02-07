from djoser.views import UserViewSet
from rest_framework import filters
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.serializers import IngredientSerializer, TagSerializer
from recipes.models import Ingredient, Tag


class TagViewSet(ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ("^name",)


class CustomUserViewSet(UserViewSet):
    ...
