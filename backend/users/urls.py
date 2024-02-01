from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import CustomUserViewSet


app_name = "users"


router = DefaultRouter()
router.register("", CustomUserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
]
