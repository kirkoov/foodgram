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
    image = Base64ImageField(required=True, allow_null=False)
    ingredients = RecipeIngredientSerializer(
        read_only=True, many=True, source="recipe_ingredient"
    )
    # is_favorited = serializers.SerializerMethodField()
    # is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            # "is_favorited",
            # "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )


class RecipeWriteSerializer(serializers.ModelSerializer):
    """[summary]

    [description]
    """

    #     ingredients = RecipeIngredientWriteSerializer(many=True, required=True)
    #     tags = serializers.PrimaryKeyRelatedField(
    #         many=True, required=True, queryset=Tag.objects.all()
    #     )
    #     image = Base64ImageField()
    #     cooking_time = serializers.IntegerField(
    #         min_value=FIELD_MIN_VALUE,
    #         max_value=FIELD_MAX_VALUE,
    #         error_messages={
    #             "min_value": f"min {FIELD_MIN_VALUE}",
    #             "max_value": f"max {FIELD_MAX_VALUE}",
    #         },
    #     )

    class Meta:  # Remove later?
        model = Recipe
        fields = (
            "ingredients",
            "tags",
            "image",
            "name",
            "text",
            "cooking_time",
        )


#     def validate(self, attrs):
#         ingredients = attrs.get("ingredients")
#         if not ingredients:
#             raise serializers.ValidationError("Ингредиент отсутствует")
#         if len(set(ingredient["id"] for ingredient in ingredients)) != len(
#             ingredients
#         ):
#             raise serializers.ValidationError("Ингредиенты повторяются")

#         if not (attrs.get("tags")):
#             raise serializers.ValidationError("Тэг отсутствует")
#         return attrs

#     def validate_image(self, image):
#         if not image:
#             raise serializers.ValidationError("Картинка отсутствует")
#         return image

#     def validate_tags(self, tags):
#         """Проверка тэга."""
#         tags_count = len(tags)
#         if tags_count != len(set(tags)):
#             raise serializers.ValidationError("Тэги повторяются")
#         return tags

#     def add_ingredients(self, recipe, ingredients):
#         prepared_write_ingredients = [
#             RecipeIngredient(
#                 recipe=recipe,
#                 ingredient=ingredient.get("id"),
#                 amount=ingredient.get("amount"),
#             )
#             for ingredient in ingredients
#         ]
#         RecipeIngredient.objects.bulk_create(prepared_write_ingredients)

#     def create(self, validated_data):
#         tags = validated_data.pop("tags")
#         ingredients = validated_data.pop("ingredients")
#         recipe = Recipe.objects.create(
#             **validated_data, author=self.context.get("request").user
#         )
#         self.add_ingredients(recipe, ingredients)
#         recipe.tags.set(tags)
#         return recipe

#     def update(self, instance, validated_data):
#         instance.ingredients.clear()
#         self.add_ingredients(instance, validated_data.pop("ingredients"))
#         instance.tags.clear()
#         instance.tags.set(validated_data.pop("tags"))
#         return super().update(instance, validated_data)

#     def to_representation(self, instance):
#         return RecipesSerializer(instance, context=self.context).data
