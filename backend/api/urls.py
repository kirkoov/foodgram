from rest_framework import routers

from django.urls import include, re_path

from api.views import (
    CustomUserViewSet,
    FavoriteViewSet,
    RecipeViewSet,
    IngredientViewSet,
    ShoppingCartViewSet,
    subscribe_user,
    TagViewSet,
)


app_name = "api"


router_v1 = routers.DefaultRouter()
router_v1.register(r"tags", TagViewSet, basename="tags")
router_v1.register(r"ingredients", IngredientViewSet, basename="ingredients")
router_v1.register(r"recipes", RecipeViewSet, basename="recipes")
router_v1.register(
    r"recipes/(?P<id>\d+)/favorite",
    FavoriteViewSet,
    basename="favorite",
)
router_v1.register(
    r"recipes/(?P<id>\d+)/shopping_cart",
    ShoppingCartViewSet,
    basename="shopping_cart",
)
router_v1.register(r"users", CustomUserViewSet, basename="users")

urlpatterns = [
    re_path(r"auth/", include("djoser.urls")),
    re_path(r"auth/", include("djoser.urls.authtoken")),
    re_path(
        r"users/(?P<id>\d+)/subscribe", subscribe_user, name="subscribe_user"
    ),
    re_path(r"", include(router_v1.urls)),
]
