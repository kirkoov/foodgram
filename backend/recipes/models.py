from typing import Optional

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


from recipes import validators


User = get_user_model()


class RecipeQuerySet(models.QuerySet):
    def add_user_annotations(self, user_id: Optional[int]):
        return self.annotate(
            is_favorite=models.Exists(
                Favorite.objects.filter(
                    user_id=user_id, recipe__pk=models.OuterRef("pk")
                )
            ),
        )


class Ingredient(models.Model):
    name = models.CharField(
        max_length=settings.NUM_CHARS_INGREDIENT_NAME,
        verbose_name=_("ingredient name"),
        help_text=_("Enter a unique ingredient name"),
    )
    measurement_unit = models.CharField(
        max_length=settings.NUM_CHARS_MEASUREMENT_UNIT,
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
        max_length=settings.NUM_CHARS_MEALTIME_NAME,
        unique=True,
        verbose_name=_("occasion name"),
        help_text=_("Enter an occasion to eat on, e.g. breakfast, etc."),
    )
    color = models.CharField(
        max_length=settings.NUM_CHARS_MEALTIME_HEX,
        validators=[validators.validate_hex_color],
        null=True,
        blank=True,
        unique=True,
        verbose_name=_("colour"),
        help_text=_("Enter a unique HEX value with the #"),
    )
    slug = models.SlugField(
        max_length=settings.NUM_CHARS_MEALTIME_SLUG,
        null=True,
        blank=True,
        unique=True,
        verbose_name=_("slug"),
        help_text=_("Enter a unique slug"),
    )

    class Meta:
        # ordering = ("name",)
        verbose_name = _("mealtime")
        verbose_name_plural = _("mealtimes")

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    amount = models.PositiveIntegerField(
        verbose_name=_("quantity"),
        help_text=_("Enter a quantity of this to use in cooking"),
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name=_("ingredient")
    )
    recipe = models.ForeignKey(
        "Recipe", on_delete=models.CASCADE, verbose_name=_("recipe")
    )

    class Meta:
        ordering = ("amount",)
        verbose_name = _("recipe ingredient")
        verbose_name_plural = _("recipe ingredients")
        default_related_name = "recipe_ingredient"

    def __str__(self):
        return f"{self.ingredient} -> {self.recipe}"


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name=_("custom user"),
    )
    recipe = models.ForeignKey(
        "Recipe",
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name=_("recipe"),
    )

    class Meta:
        ordering = ("user",)
        verbose_name = _("favourite")
        verbose_name_plural = _("favourites")
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_favorite_user_recipe"
            )
        ]

    def __str__(self):
        return f"{self.user} 😋 {self.recipe}"


class Recipe(models.Model):
    # "is_in_shopping_cart": true,
    name = models.CharField(
        max_length=settings.NUM_CHARS_RECIPE_NAME,
        verbose_name=_("recipe name"),
        help_text=_("Enter a name for your recipe"),
    )
    image = models.ImageField(
        upload_to="recipes/",
        default=None,
        verbose_name=_("recipe image"),
        help_text=_("Upload a <=3MB image for your recipe"),
    )
    text = models.TextField(
        verbose_name=_("recipe description"),
        help_text=_("Describe how to cook"),
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(settings.MIN_COOKING_TIME_MINS),
            MaxValueValidator(settings.MAX_COOKING_TIME_MINS),
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

    objects = RecipeQuerySet.as_manager()

    class Meta:
        ordering = ("name",)
        verbose_name = _("recipe")
        verbose_name_plural = _("recipes")

    def __str__(self):
        return self.name


# class Subscription(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name="subscribed_to",
#         verbose_name="Подписчик",
#     )
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name="subscribed_by",
#         verbose_name="Автор",
#     )

#     def __str__(self):
#         return f"Подписка {self.user} на {self.author}"
