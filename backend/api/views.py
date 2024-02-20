from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import filters, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from django.contrib.auth import get_user_model

from .filters import IngredientFilter, RecipeFilter
from .serializers import (
    CustomUserSerializer,
    FavoriteSerializer,
    IngredientSerializer,
    RecipeSerializer,
    RecipeWriteSerializer,
    TagSerializer,
)
from recipes.models import Favorite, Ingredient, Recipe, Tag
from users.models import CustomUser


User = get_user_model()


class CustomPagination(PageNumberPagination):
    page_size_query_param = "limit"


class RecipeViewSet(ModelViewSet):
    http_method_names = ("get", "post", "patch", "delete")
    serializer_class = RecipeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    #     IsAuthorOrReadOnly,
    filterset_class = RecipeFilter
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Recipe.objects.prefetch_related(
            "author",
            "tags",
            "ingredients",
            "recipe_ingredient__ingredient",
        )
        if self.request.user.is_authenticated:
            queryset = queryset.add_user_annotations(self.request.user.id)
        return queryset

    # def perform_create(self, srlzr):
    #     srlzr.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return RecipeSerializer
        return RecipeWriteSerializer


class FavoriteViewSet(ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None

    def get_queryset(self):
        print(self.request.user.id)
        queryset = Favorite.objects.all()
        # queryset = Recipe.objects.prefetch_related(
        #     "author",
        #     "tags",
        #     "ingredients",
        #     "recipe_ingredient__ingredient",
        # )
        # if self.request.user.is_authenticated:
        #     queryset = queryset.add_user_annotations(self.request.user.id)
        return queryset


class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("slug",)
    pagination_class = None
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class IngredientViewSet(ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    pagination_class = None
    filterset_class = IngredientFilter
    permission_classes = (permissions.AllowAny,)


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    pagination_class = CustomPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # @action(
    #     methods=["get"],
    #     url_path="me",
    #     detail=False,
    #     permission_classes=(permissions.IsAuthenticated,),
    # )
    # def me(self, request):
    #     serializer = CustomUserSerializer(request.user)
    #     if request.user.is_authenticated:
    #         return Response(serializer.data)
    #     return Response(status=status.HTTP_401_UNAUTHORIZED)

    def get_permissions(self):
        if self.action == "me":
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()
