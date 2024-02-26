from rest_framework.authtoken.models import TokenProxy

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .models import User, Subscription


@admin.register(User)
class UsersAdmin(UserAdmin):
    list_display = (
        "pk",
        "email",
        "username",
        "first_name",
        "count_recipes",
        "count_subscriptions",
    )
    list_filter = ("email", "username")
    empty_value_display = _("empty")

    @admin.display(
        description=_("recipes"),
    )
    def count_recipes(self, obj):
        return obj.recipes.count()

    @admin.display(
        description=_("subscriptions"),
    )
    def count_subscriptions(self, obj):
        return obj.is_subscriber.count()


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "author",
    )


admin.site.unregister(Group)
admin.site.unregister(TokenProxy)
