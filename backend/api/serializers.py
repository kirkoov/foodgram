from django.utils.translation import gettext_lazy as _
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)
from rest_framework import serializers, status
from users.models import Subscription, User

from backend.constants import MAX_INGREDIENT_AMOUNT, MIN_INGREDIENT_AMOUNT


class UsersSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        return (
            request.user.is_authenticated and request.user.is_subscriber.all().exists()
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Read ingredients."""

    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(source="ingredient.measurement_unit")

    class Meta:
        model = RecipeIngredient
        fields = ("id", "name", "measurement_unit", "amount")


class RecipeIngredientWriteSerializer(serializers.ModelSerializer):
    """Write ingredients."""

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(
        min_value=MIN_INGREDIENT_AMOUNT,
        max_value=MAX_INGREDIENT_AMOUNT,
    )

    class Meta:
        model = RecipeIngredient
        fields = ("id", "amount")


class AbridgedRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")
        read_only_fields = fields


class RecipeSerializer(serializers.ModelSerializer):
    """Read a recipe."""

    author = UsersSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    image = Base64ImageField(required=True)
    # image = Base64ImageField(required=True, allow_null=False)
    ingredients = RecipeIngredientSerializer(
        read_only=True, many=True, source="recipe_ingredient"
    )
    is_favorited = serializers.BooleanField(default=False)
    is_in_shopping_cart = serializers.BooleanField(default=False)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(recipe=obj, user=self.request.user).exists()


class RecipeWriteSerializer(serializers.ModelSerializer):
    """Add a recipe."""

    ingredients = RecipeIngredientWriteSerializer(many=True, required=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, required=True, queryset=Tag.objects.all()
    )
    image = Base64ImageField(required=True)

    class Meta:
        model = Recipe
        fields = (
            "ingredients",
            "tags",
            "image",
            "name",
            "text",
            "cooking_time",
        )

    def do_ingredients(self, recipe, ingredients):
        ingredients = [
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient["id"],
                amount=ingredient["amount"],
            )
            for ingredient in ingredients
        ]
        RecipeIngredient.objects.bulk_create(ingredients)

    def create(self, validated_data):
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(
            **validated_data, author=self.context.get("request").user
        )
        self.do_ingredients(recipe, ingredients)
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        instance.ingredients.clear()
        self.do_ingredients(instance, validated_data.pop("ingredients"))
        instance.tags.clear()
        instance.tags.set(validated_data.pop("tags"))
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeSerializer(instance, context=self.context).data


class FavoriteSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = ("user", "recipe", "is_favorited")

    def get_is_favorited(self, obj):
        request = self.context["request"]
        return (
            request.user.is_authenticated
            and Favorite.objects.filter(user=request.user, recipe=obj.pk).exists()
        )


class ShoppingCartSerializer(serializers.ModelSerializer):
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCart
        fields = ("user", "recipe", "is_in_shopping_cart")

    def get_is_in_shopping_cart(self, obj):
        request = self.context["request"]
        return (
            request.user.is_authenticated
            and ShoppingCart.objects.filter(user=request.user, recipe=obj.pk).exists()
        )


class SubscriptionSerializer(UsersSerializer):
    """Read a subscription."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(source="recipes.count")

    class Meta(UsersSerializer.Meta):
        fields = (  # type: ignore[assignment]
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def get_recipes(self, obj):
        request = self.context.get("request")
        recipes_limit = request.query_params.get("recipes_limit")
        recipes = obj.recipes.all()
        if recipes_limit and recipes_limit.isdigit():
            recipes = recipes[: int(recipes_limit)]
        serializer = AbridgedRecipeSerializer(
            recipes, many=True, context={"request": request}
        )
        return serializer.data

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        return (
            user.is_authenticated
            and user.is_subscriber.all().filter(author=obj.pk).exists()
        )


class SubscriptionWriteSerializer(serializers.ModelSerializer):
    """Add a subscription."""

    class Meta:
        model = Subscription
        fields = ("user", "author")

    def validate(self, data):
        try:
            user_id = data.get("user").id
            author_id = data.get("author").id
        except AttributeError:
            raise serializers.ValidationError(
                detail=_("Wrong user or author details."),
                code=status.HTTP_400_BAD_REQUEST,
            )
        if Subscription.objects.filter(author=author_id, user=user_id).exists():
            raise serializers.ValidationError(
                detail=_("This subscription exists already."),
                code=status.HTTP_400_BAD_REQUEST,
            )
        if user_id == author_id:
            raise serializers.ValidationError(
                detail=_("You can't subscribe to yourself."),
                code=status.HTTP_400_BAD_REQUEST,
            )
        return data
