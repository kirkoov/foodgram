from typing import Optional

from django.conf import settings
from django.contrib.auth import get_user_model
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
                name="Unique ingredient-measure constraint",
            ),
        )

    def __str__(self):
        return f"{self.name} ({self.measurement_unit})"


class Tag(models.Model):
    name = models.CharField(
        max_length=settings.NUM_CHARS_MEALTIME_NAME,
        unique=True,
        verbose_name=_("occasion name"),
        help_text=_("Enter an occasion to eat: breakfast, lunch or dinner"),
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
        ordering = ("name",)
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

    def __str__(self):
        return f"{self.ingredient} -> {self.recipe}"


# class Favorite(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name="favorites",
#         verbose_name=_("custom user"),
#     )
#     recipe = models.ForeignKey(
#         "Recipe",
#         on_delete=models.CASCADE,
#         related_name="favorites",
#         verbose_name=_("recipe"),
#     )

#     class Meta:
#         ordering = ("user",)
#         verbose_name = _("favourite")
#         verbose_name_plural = _("favourites")
#         constraints = [
#             models.UniqueConstraint(
#                 fields=["user", "recipe"], name="unique_favorite_user_recipe"
#             )
#         ]

#     def __str__(self):
#         return f"{self.user} 😋 {self.recipe}"


class Recipe(models.Model):
    # tags,
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name=_("author"),
    )
    name = models.CharField(
        max_length=settings.NUM_CHARS_RECIPE_NAME,
        verbose_name=_("recipe name"),
        help_text=_("Enter a name for your recipe"),
    )
    text = models.TextField(
        verbose_name=_("recipe description"),
        help_text=_("Describe how to cook"),
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through=RecipeIngredient,
        through_fields=("recipe", "ingredient"),
        verbose_name=_("ingredients"),
    )

    objects = RecipeQuerySet.as_manager()

    class Meta:
        ordering = ("name",)
        verbose_name = _("recipe")
        verbose_name_plural = _("recipes")

    def __str__(self):
        return self.name
