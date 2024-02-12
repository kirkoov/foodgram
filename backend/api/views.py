from djoser.views import UserViewSet
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.serializers import (
    CustomUserSerializer,
    IngredientSerializer,
    TagSerializer,
)
from recipes.models import Ingredient, Tag
from users.models import CustomUser


class CustomPagination(PageNumberPagination):
    page_size_query_param = "limit"


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


# class CustomUserViewSet(UserViewSet):
#     ...


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    pagination_class = CustomPagination
