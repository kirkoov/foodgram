from djoser.serializers import UserSerializer
from rest_framework import serializers

from recipes.models import Ingredient, Tag
from users.models import CustomUser


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        # request = self.context.get("request")
        # return (
        #     request.user.is_authenticated
        #     and Subscribe.objects.filter(
        #         user=request.user, author=obj
        #     ).exists()
        # )
        return False

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )
