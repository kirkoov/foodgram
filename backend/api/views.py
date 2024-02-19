from djoser.views import UserViewSet
from rest_framework import filters, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers import (
    CustomUserSerializer,
    IngredientSerializer,
    RecipeSerializer,
    RecipeWriteSerializer,
    TagSerializer,
)
from recipes.models import Ingredient, Recipe, Tag
from users.models import CustomUser


User = get_user_model()


class CustomPagination(PageNumberPagination):
    page_size_query_param = "limit"


class RecipeViewSet(ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # permission_classes = (
    #     permissions.IsAuthenticatedOrReadOnly,
    #     IsAuthorOrReadOnly,
    # )

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("tags", "author")
    # pagination_class = LimitPagination
    # filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return RecipeSerializer
        return RecipeWriteSerializer


class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class IngredientViewSet(ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ("^name",)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


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
