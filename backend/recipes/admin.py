from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Subscription,
    Tag,
)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "measurement_unit")
    list_filter = ("name", "measurement_unit")
    ordering = ("name",)
    empty_value_display = _("empty")


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "author")
    ordering = ("name",)
    empty_value_display = _("empty")


class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "output_order")
    ordering = ("name",)
    empty_value_display = _("empty")


admin.site.register(Favorite)
admin.site.register(ShoppingCart)
admin.site.register(Subscription)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngredient)
