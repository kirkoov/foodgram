from backend.constants import (
    MAX_COOKING_TIME_MINS,
    MAX_INGREDIENT_AMOUNT,
    MIN_COOKING_TIME_MINS,
    MIN_INGREDIENT_AMOUNT,
    NUM_CHARS_INGREDIENT_NAME,
    NUM_CHARS_MEALTIME_HEX,
    NUM_CHARS_MEALTIME_NAME,
    NUM_CHARS_MEALTIME_SLUG,
    NUM_CHARS_MEASUREMENT_UNIT,
    NUM_CHARS_RECIPE_NAME,
)
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from recipes import validators

from .validators import validate_img_size

User = get_user_model()


class RecipeQuerySet(models.QuerySet):
    def add_user_annotations(self, user_id: str | int):
        return self.annotate(
            is_favorited=models.Exists(
                Favorite.objects.filter(
                    user_id=user_id, recipe__pk=models.OuterRef("pk")
                )
            ),
            is_in_shopping_cart=models.Exists(
                ShoppingCart.objects.filter(
                    user_id=user_id, recipe__pk=models.OuterRef("pk")
                )
            ),
        )

    def filter_on_tags(self, tags):
        if tags:
            return self.filter(tags__slug__in=tags).distinct()
        return self


class Ingredient(models.Model):
    name = models.CharField(
        max_length=NUM_CHARS_INGREDIENT_NAME,
        verbose_name=_("ingredient name"),
        help_text=_("Enter a unique ingredient name"),
    )
    measurement_unit = models.CharField(
        max_length=NUM_CHARS_MEASUREMENT_UNIT,
        verbose_name=_("measurement unit"),
        help_text=_("In grams, pieces, to taste, etc"),
    )

    class Meta:
        ordering = ("name",)
        verbose_name = _("ingredient")
        verbose_name_plural = _("ingredients")
        constraints = (
            models.UniqueConstraint(
                fields=("name", "measurement_unit"),
                name="unique_ingredient_measurement_unit",
            ),
        )

    def __str__(self):
        return f"{self.name} ({self.measurement_unit})"


class Tag(models.Model):
    name = models.CharField(
        max_length=NUM_CHARS_MEALTIME_NAME,
        unique=True,
        verbose_name=_("occasion name"),
        help_text=_("Enter an occasion to eat on, e.g. breakfast, etc."),
    )
    color = models.CharField(
        max_length=NUM_CHARS_MEALTIME_HEX,
        validators=[validators.validate_hex_color],
        unique=True,
        verbose_name=_("colour"),
        help_text=_("Enter a unique HEX value with the #"),
    )
    slug = models.SlugField(
        max_length=NUM_CHARS_MEALTIME_SLUG,
        validators=[validators.validate_slug_field],
        unique=True,
        verbose_name=_("slug"),
        help_text=_("Enter a unique slug"),
    )

    class Meta:
        verbose_name = _("mealtime")
        verbose_name_plural = _("mealtimes")

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    amount = models.PositiveSmallIntegerField(
        verbose_name=_("quantity"),
        help_text=_("Enter a quantity of this to use in cooking"),
        validators=[
            MinValueValidator(MIN_INGREDIENT_AMOUNT),
            MaxValueValidator(MAX_INGREDIENT_AMOUNT),
        ],
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.RESTRICT, verbose_name=_("ingredient")
    )
    recipe = models.ForeignKey(
        "Recipe", on_delete=models.CASCADE, verbose_name=_("recipe")
    )

    class Meta:
        verbose_name = _("recipe ingredient")
        verbose_name_plural = _("recipe ingredients")
        default_related_name = "recipe_ingredient"
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="unique_recipe_ingredient",
            )
        ]

    def __str__(self):
        return f"{self.recipe.name}:{self.ingredient.name}"


class BaseFavoriteShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("custom user"),
        related_name="%(class)s",
    )
    recipe = models.ForeignKey(
        "Recipe",
        on_delete=models.CASCADE,
        verbose_name=_("recipe"),
        related_name="%(class)s",
    )

    class Meta:
        abstract = True
        ordering = ("user",)

    def __str__(self):
        return f"{self.user}@{self.recipe}"


class Favorite(BaseFavoriteShoppingCart):
    class Meta(BaseFavoriteShoppingCart.Meta):
        verbose_name = _("favourite")
        verbose_name_plural = _("favourites")


class ShoppingCart(BaseFavoriteShoppingCart):
    class Meta(BaseFavoriteShoppingCart.Meta):
        verbose_name = _("shopping_cart")
        verbose_name_plural = _("shopping_carts")
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_shopping_user_recipe"
            )
        ]


class Recipe(models.Model):
    name = models.CharField(
        max_length=NUM_CHARS_RECIPE_NAME,
        verbose_name=_("recipe name"),
        help_text=_("Enter a name for your recipe"),
    )
    image = models.ImageField(
        validators=[validate_img_size],
        upload_to="recipes/",
        verbose_name=_("recipe image"),
        help_text=_("Upload an image<=1MB for your recipe"),
    )
    text = models.TextField(
        verbose_name=_("recipe description"),
        help_text=_("Describe how to cook"),
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(MIN_COOKING_TIME_MINS),
            MaxValueValidator(MAX_COOKING_TIME_MINS),
        ],
        verbose_name=_("cooking time"),
        help_text=_("Enter now many minutes it needs to cook"),
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_("mealtimes"),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name=_("author"),
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through=RecipeIngredient,
        verbose_name=_("ingredients"),
    )
    pub_date = models.DateTimeField(_("published on"), auto_now_add=True)

    objects = RecipeQuerySet.as_manager()

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = _("recipe")
        verbose_name_plural = _("recipes")
        default_related_name = "recipes"

    def __str__(self):
        return self.name
