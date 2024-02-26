from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.rl_config import TTFSearchPath  # type: ignore[import-untyped]
from rest_framework import permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from django.conf import settings
from django.db.models import Sum
from django.http import FileResponse, Http404
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from .filters import IngredientFilter, RecipeFilter
from .paginations import LimitPagination
from .serializers import (
    AbridgedRecipeSerializer,
    UsersSerializer,
    FavoriteSerializer,
    IngredientSerializer,
    RecipeSerializer,
    RecipeWriteSerializer,
    ShoppingCartSerializer,
    SubscriptionSerializer,
    SubscriptionWriteSerializer,
    TagSerializer,
)
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)
from users.models import Subscription


User = get_user_model()


class RecipeViewSet(ModelViewSet):
    http_method_names = ("get", "post", "patch", "delete")
    serializer_class = RecipeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filterset_class = RecipeFilter
    pagination_class = LimitPagination

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

    def create_shopping_list_pdf(self, shoppings):
        X_ITEM = 30
        X_QNTY = 380
        X_UNITS = 450

        try:
            TTFSearchPath.append(str(settings.BASE_DIR) + "/data/fonts")
            buffer = io.BytesIO()
            p = canvas.Canvas(buffer, pagesize=A4)
            p.drawImage(
                "fg_logo_for_shopping_list.png", 30, 790, width=20, height=20
            )
            pdfmetrics.registerFont(TTFont("Fira", "FiraCode-Regular.ttf"))
            p.setFont("Fira", 12)
            p.drawRightString(550, 800, "Shopping list, Foodgram")
            p.drawString(X_ITEM, 750, "Item")
            p.drawString(X_QNTY, 750, "Qnty")
            p.drawString(X_UNITS, 750, "Units")
            i = 15
            y = 730
            for item, details in shoppings.items():
                p.drawString(X_ITEM, y, item)
                p.drawString(X_QNTY, y, str(details[0]))
                p.drawString(X_UNITS, y, details[1])
                y -= i
            p.showPage()
            p.save()
            buffer.seek(0)
            return buffer
        except Exception as e:
            return Response(
                f"Some error occurred while creating your shoppings list: {e}",
                status=status.HTTP_204_NO_CONTENT,
            )

    @action(
        methods=["get"],
        detail=False,
        url_path="download_shopping_cart",
        permission_classes=[permissions.IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        try:
            shopping_totals = (
                RecipeIngredient.objects.filter(
                    recipe__shoppingcart__user=self.request.user
                )
                .values("ingredient__name", "ingredient__measurement_unit")
                .annotate(quantity=Sum("amount"))
            )
            shoppings = {
                item["ingredient__name"]: [
                    item["quantity"],
                    item["ingredient__measurement_unit"],
                ]
                for item in shopping_totals
            }
        except Exception as e:
            return Response(
                f"Some error occurred in extracting your shopping data: {e}",
                status=status.HTTP_204_NO_CONTENT,
            )

        return FileResponse(
            self.create_shopping_list_pdf(shoppings),
            as_attachment=True,
            filename="my-Foodgram_shopping-list.pdf",
        )


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


class TagViewSet(ReadOnlyModelViewSet):
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


class UsersViewSet(UserViewSet):
    serializer_class = UsersSerializer
    queryset = User.objects.all()
    pagination_class = LimitPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_permissions(self):
        if self.action == "me":
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    @action(
        methods=["get"],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
    )
    def subscriptions(self, request):
        curr_user = request.user
        subscriptions = User.objects.filter(is_subscribed__user=curr_user)
        paginator = self.paginate_queryset(subscriptions)
        serializer = SubscriptionSerializer(
            paginator, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)


@api_view(["POST", "DELETE"])
@permission_classes([permissions.IsAuthenticated])
def subscribe_user(request, id):
    user = request.user
    author = get_object_or_404(User, id=id)
    if request.method == "DELETE":
        try:
            subscription = get_object_or_404(
                Subscription, user=user, author=author
            )
            subscription.delete()
            return Response(
                {"success": _("Subscription deleted.")},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Http404:
            return Response(
                {"errors": _("No subscription to delete.")},
                status=status.HTTP_400_BAD_REQUEST,
            )
    recipes_limit = request.query_params.get("recipes_limit")
    serializer = SubscriptionWriteSerializer(
        data={"user": user.id, "author": author.id},
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    recipes = Recipe.objects.filter(author=author)
    if recipes_limit:
        recipes = recipes[: int(recipes_limit)]
    serializer = UsersSerializer(user, context={"request": request})
    data = serializer.data
    data["recipes"] = AbridgedRecipeSerializer(recipes, many=True).data
    data["recipes_count"] = len(recipes)

    return Response(
        data,
        status=status.HTTP_201_CREATED,
    )
