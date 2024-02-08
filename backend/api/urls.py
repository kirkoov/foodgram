from rest_framework import routers

from django.urls import include, path

from api.views import CustomUserViewSet, IngredientViewSet, TagViewSet


app_name = "api"


router_v1 = routers.DefaultRouter()
router_v1.register(r"tags", TagViewSet, basename="tags")
router_v1.register(r"ingredients", IngredientViewSet, basename="ingredients")
router_v1.register(r"users", CustomUserViewSet, basename="users")

urlpatterns = [
    path(r"auth/", include("djoser.urls")),
    path(r"auth/", include("djoser.urls.jwt")),
    path(r"", include(router_v1.urls)),
]
