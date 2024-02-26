from django.contrib import admin

from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .forms import TagForm
from .models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)


class RecipeIngredientsShowInLine(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    min_num = 1


@admin.register(Ingredient)
class Ingredients(admin.ModelAdmin):
    list_display = ("id", "name", "measurement_unit")
    list_filter = ("name", "measurement_unit")
    ordering = ("name",)
    search_fields = ("name",)
    empty_value_display = _("empty")


@admin.register(Recipe)
class Recipes(admin.ModelAdmin):
    list_display = ("id", "pic_preview", "name", "author", "pub_date")
    list_filter = ("name", "author", "tags")
    ordering = ("name",)
    search_fields = ("name",)
    inlines = (RecipeIngredientsShowInLine,)
    filter_horizontal = ("tags",)
    empty_value_display = _("empty")

    @admin.display(
        description=_("pic"),
    )
    def pic_preview(self, obj):
        if obj.image:
            return format_html(
                f'<img src="{obj.image.url}" width=40 height=40 />'
            )
        return format_html("")


@admin.register(ShoppingCart)
class ShoppingCarts(admin.ModelAdmin):
    ordering = ("recipe__pub_date",)
    list_display = ("id", "user", "recipe")
    list_filter = ("user",)
    search_fields = ("user__username", "recipe__name")
    empty_value_display = _("empty")


@admin.register(RecipeIngredient)
class RecipeIngredients(admin.ModelAdmin):
    ordering = ("recipe__id",)
    list_display = ("id", "recipe", "ingredient", "amount")
    list_filter = ("ingredient", "recipe")
    search_fields = ("ingredient_name", "recipe__name")
    empty_value_display = _("empty")


@admin.register(Favorite)
class Favorites(admin.ModelAdmin):
    list_display = ("user", "recipe")
    list_filter = ("user", "recipe__tags")
    ordering = ("recipe__pub_date",)
    search_fields = ("user__username", "recipe__name")
    empty_value_display = _("empty")


@admin.register(Tag)
class Tags(admin.ModelAdmin):
    form = TagForm
    list_display = ("id", "name", "color", "slug")
    ordering = ("name",)
    search_fields = ("name",)
    empty_value_display = _("empty")
