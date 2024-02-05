from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from recipes import validators

# class Recipe(models.Model):
#     ...


# class RecipeIngredient(models.Model):
#     ...


# class Favorite(models.Model):
#     ...


class Ingredient(models.Model):
    name = models.CharField(
        max_length=settings.NUM_CHARS_INGREDIENT_NAME,
        verbose_name=_("ingredient name"),
        unique=True,
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
