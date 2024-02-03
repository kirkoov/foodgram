from rest_framework import routers

from django.urls import include, path

from api.views import TagViewSet


router_v1 = routers.DefaultRouter()
router_v1.register(r"tags", TagViewSet)

urlpatterns = [
    path(r"auth", include("djoser.urls")),
    path(r"auth", include("djoser.urls.authtoken")),
    path(r"", include(router_v1.urls)),
]

# path("users/", include("users.urls", namespace="users"))
