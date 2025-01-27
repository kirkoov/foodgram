import io

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.rl_config import TTFSearchPath  # type: ignore[import-untyped]
from rest_framework import permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from users.models import Subscription

from .filters import IngredientFilter, RecipeFilter
from .paginations import LimitPagination
from .permissions import IsAuthorOrReadOnly, ReadOnly
from .serializers import (
    AbridgedRecipeSerializer,
    FavoriteSerializer,
    IngredientSerializer,
    RecipeSerializer,
    RecipeWriteSerializer,
    ShoppingCartSerializer,
    SubscriptionSerializer,
    SubscriptionWriteSerializer,
    TagSerializer,
    UsersSerializer,
)

User = get_user_model()


class RecipeViewSet(ModelViewSet):
    http_method_names = ("get", "post", "patch", "delete")
    serializer_class = RecipeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filterset_class = RecipeFilter
    pagination_class = LimitPagination

    def get_permissions(self):
        if self.action == "patch" or self.action == "delete":
            # self.permission_classes = (IsAuthorOrReadOnly,)
            return (IsAuthorOrReadOnly(),)
        elif self.action == "retrieve":
            return (ReadOnly(),)
        return super().get_permissions()

    def get_queryset(self):
        """Use the prefetch_related() to rid of duplicate requests."""
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
        """Choose a serializer given the method."""
        if self.action in ("list", "retrieve"):
            return RecipeSerializer
        return RecipeWriteSerializer

    def create_shopping_list_pdf(self, shoppings):
        """Draw the FG icon & then the shopping list strings."""
        x_item = 30
        x_qnty = 380
        x_units = 450

        TTFSearchPath.append(str(settings.BASE_DIR) + "/data/fonts/")
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        p.drawImage(
            "fg_logo_for_shopping_list.png", 30, 790, width=20, height=20
        )
        pdfmetrics.registerFont(TTFont("DejaVuSans", "DejaVuSans.ttf"))
        pdfmetrics.registerFont(
            TTFont("DejaVuSansBold", "DejaVuSans-Bold.ttf")
        )
        p.setFont("DejaVuSans", 12)
        p.drawRightString(550, 800, "Shopping list, Foodgram")
        p.setFont("DejaVuSansBold", 10)
        p.drawString(x_item, 750, "Item")
        p.drawString(x_qnty, 750, "Qnty")
        p.drawString(x_units, 750, "Units")
        p.setFont("DejaVuSans", 12)
        i = 15
        y = 730
        for item, details in sorted(shoppings.items()):
            p.drawString(x_item, y, item)
            p.drawString(x_qnty, y, str(details[0]))
            p.drawString(x_units, y, details[1])
            y -= i
        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer

    @action(
        methods=["post"],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
    )
    def favorite(self, request, pk):
        return self.add_recipe(
            FavoriteSerializer, request, get_object_or_404(Recipe, pk=pk)
        )

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.remove_recipe(
            Favorite, request.user, get_object_or_404(Recipe, pk=pk)
        )

    @action(
        methods=["post"],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
    )
    def shopping_cart(self, request, pk):
        return self.add_recipe(
            ShoppingCartSerializer, request, get_object_or_404(Recipe, pk=pk)
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.remove_recipe(
            ShoppingCart, request.user, get_object_or_404(Recipe, pk=pk)
        )

    @action(
        methods=["get"],
        detail=False,
        url_path="download_shopping_cart",
        permission_classes=[permissions.IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        """Download as an attachment, with opening it too in the browser."""
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

    @staticmethod
    def add_recipe(serializer, request, recipe):
        srlzr = serializer(
            data={"user": request.user.id, "recipe": recipe.id},
            context={"request": request},
        )
        srlzr.is_valid(raise_exception=True)
        srlzr.save()
        return Response(srlzr.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def remove_recipe(model, user, recipe):
        get_object_or_404(model, user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BaseFavoriteShoppingCartViewSet(ModelViewSet):
    model: type[Favorite] | type[ShoppingCart] | None
    serializer_class: (
        type[FavoriteSerializer] | type[ShoppingCartSerializer] | None
    )

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


class ShoppingCartViewSet(BaseFavoriteShoppingCartViewSet):
    model = ShoppingCart
    serializer_class = ShoppingCartSerializer
    queryset = ShoppingCart.objects.all()
    permission_classes = (permissions.AllowAny,)


class TagViewSet(ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("slug",)
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    pagination_class = None
    filterset_class = IngredientFilter
    permission_classes = (permissions.AllowAny,)


class UsersViewSet(UserViewSet):
    """Use Djoser's."""

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
def subscribe_user(request, i_d):
    user = request.user
    author = get_object_or_404(User, id=i_d)
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
