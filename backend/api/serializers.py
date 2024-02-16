import base64
from djoser.serializers import UserSerializer
from rest_framework import serializers

from django.conf import settings
from django.core.files.base import ContentFile

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from users.models import CustomUser


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)

        return super().to_internal_value(data)


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


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """[summary]

    [description]

    Attributes:
        id -- [description]
        name -- [description]
        measurement_unit -- [description]
        ) -- [description]
    """

    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = RecipeIngredient
        fields = ("id", "name", "measurement_unit", "amount")


class RecipeIngredientWriteSerializer(serializers.ModelSerializer):
    """[summary]

    [description]

    Attributes:
        id -- [description]
        amount -- [description]
        ) -- [description]
    """

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(
        min_value=settings.MIN_INGREDIENT_AMOUNT,
        max_value=settings.MAX_INGREDIENT_AMOUNT,
    )

    class Meta:
        model = RecipeIngredient
        fields = ("id", "amount")


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)

    # image = Base64ImageField(required=True, allow_null=False)

    # ingredients = RecipeIngredientSerializer(
    #     read_only=True, many=True, source="recipeingredient"
    # )
    # is_favorited = serializers.SerializerMethodField()
    # is_in_shopping_cart = serializers.SerializerMethodField()

    # def update(self, instance, validated_data):
    #     # instance.name = validated_data.get('name', instance.name)
    #     # instance.color = validated_data.get('color', instance.color)
    #     # instance.birth_year = validated_data.get(
    #     #     'birth_year', instance.birth_year
    #     #     )
    #     instance.image = validated_data.get("image", instance.image)
    #     # if 'achievements' in validated_data:
    #     #     achievements_data = validated_data.pop('achievements')
    #     #     lst = []
    #     #     for achievement in achievements_data:
    #     #         current_achievement, status =
    #     # Achievement.objects.get_or_create(
    #     #             **achievement
    #     #             )
    #     #         lst.append(current_achievement)
    #     #     instance.achievements.set(lst)

    #     instance.save()
    #     return instance

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            # "ingredients",
            # "is_favorited",
            # "is_in_shopping_cart",
            "name",
            # "image",
            # "text",
            # "cooking_time",
        )
