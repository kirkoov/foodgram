from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
import io
from reportlab.pdfgen import canvas
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from django.http import FileResponse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from .filters import IngredientFilter, RecipeFilter
from .serializers import (
    CustomUserSerializer,
    FavoriteSerializer,
    IngredientSerializer,
    RecipeSerializer,
    RecipeWriteSerializer,
    ShoppingCartSerializer,
    TagSerializer,
)
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from users.models import CustomUser


User = get_user_model()


class CustomPagination(PageNumberPagination):
    page_size_query_param = "limit"


class RecipeViewSet(ModelViewSet):
    http_method_names = ("get", "post", "patch", "delete")
    serializer_class = RecipeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
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

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return RecipeSerializer
        return RecipeWriteSerializer

    @action(methods=["get"], detail=False, url_path="download_shopping_cart")
    def download_shopping_cart(self, request):
        # shopping_list = self.request.user.shopping.all()
        # text = "\n".join([f"{recipe.name}..." for recipe in shopping_list])
        # <QuerySet [<ShoppingCart: yummy:MeatBalls4eva>, <ShoppingCart:
        # yummy:MyNewLunch>, <ShoppingCart: yummy:PiñaColadaOrYogurt-Up2U>]
        # text = "Test text"

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 100, "Hello world.")
        p.showPage()
        p.save()
        buffer.seek(0)
        # return FileResponse(
        #     text,
        #     content_type="text/plain",
        #     as_attachment=True,
        #     filename="my_shopping_list.txt",
        # )
        return FileResponse(buffer, as_attachment=True, filename="hello.pdf")


class BaseFavoriteShoppingCartViewSet(ModelViewSet):
    model: type[Favorite] | type[ShoppingCart] | None
    serializer_class: type[FavoriteSerializer] | type[
        ShoppingCartSerializer
    ] | None

    def create(self, request, **kwargs):
        item_id = self.kwargs.get("id")
        item = get_object_or_404(Recipe, id=item_id)
        if self.model.objects.filter(user=request.user, recipe=item).exists():
            return Response(
                _("This recipe already exists."),
                status=status.HTTP_400_BAD_REQUEST,
            )
        new_item = self.model(user=request.user, recipe=item)
        new_item.save()
        serializer = self.serializer_class(
            new_item, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, **kwargs):
        item_id = self.kwargs.get("id")
        item = get_object_or_404(Recipe, id=item_id)
        if not self.model.objects.filter(
            user=request.user, recipe=item
        ).exists():
            return Response(
                _("No recipe to delete."),
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.model.objects.get(user=request.user, recipe=item).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(BaseFavoriteShoppingCartViewSet):
    model = Favorite
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()
    permission_classes = (permissions.AllowAny,)
    # pagination_class = None


class ShoppingCartViewSet(BaseFavoriteShoppingCartViewSet):
    model = ShoppingCart
    serializer_class = ShoppingCartSerializer
    queryset = ShoppingCart.objects.all()
    permission_classes = (permissions.AllowAny,)
    # pagination_class = None


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
