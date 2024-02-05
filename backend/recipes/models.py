from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from recipes import validators

# class Ingredient(models.Model):
#     name = models.CharField(max_length=100, verbose_name="...")
#     measurement_unit = models.CharField(max_length=100, verbose_name="...")

#     class Meta:
#         ...

#     def __str__(self):
#         ...


# class Recipe(models.Model):
#     ...


# class RecipeIngredient(models.Model):
#     ...


# class Favorite(models.Model):
#     ...


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
