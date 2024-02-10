from rest_framework import routers

from django.urls import include, re_path

from api.views import CustomUserViewSet, IngredientViewSet, TagViewSet


app_name = "api"


router_v1 = routers.DefaultRouter()
router_v1.register(r"tags", TagViewSet, basename="tags")
router_v1.register(r"ingredients", IngredientViewSet, basename="ingredients")
router_v1.register(r"users", CustomUserViewSet, basename="users")

urlpatterns = [
    re_path(r"auth/", include("djoser.urls")),
    re_path(r"auth/", include("djoser.urls.authtoken")),
    re_path(r"", include(router_v1.urls)),
]
