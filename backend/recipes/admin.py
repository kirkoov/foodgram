from django.contrib import admin

from recipes.models import Favourite, Ingredient, Recipe, RecipeIngredient


admin.site.register(Favourite)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
