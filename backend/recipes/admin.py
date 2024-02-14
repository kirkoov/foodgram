from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    list_filter = ("name", "measurement_unit")
    ordering = ("name",)
    empty_value_display = _("empty")


admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngredient)
