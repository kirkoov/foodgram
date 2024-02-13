from djoser.views import UserViewSet
from rest_framework import filters, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ReadOnlyModelViewSet

from django.contrib.auth import get_user_model

from api.serializers import (
    CustomUserSerializer,
    IngredientSerializer,
    TagSerializer,
)
from recipes.models import Ingredient, Tag
from users.models import CustomUser


User = get_user_model()


class CustomPagination(PageNumberPagination):
    page_size_query_param = "limit"


class TagViewSet(ReadOnlyModelViewSet):
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
