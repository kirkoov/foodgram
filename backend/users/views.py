from rest_framework import viewsets

from django.contrib.auth import get_user_model

from .models import CustomUser
from .serializers import CustomUserSerializer, CustomUserListSerializer


User = get_user_model()


class CustomUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return CustomUserListSerializer
        return CustomUserSerializer
