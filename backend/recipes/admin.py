from django.contrib import admin

# from recipes.models import Favourite, Recipe, RecipeIngredient
from recipes.models import Ingredient, Tag


admin.site.register(Tag)
admin.site.register(Ingredient)
# admin.site.register(Recipe)
# admin.site.register(RecipeIngredient)
