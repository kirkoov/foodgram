from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser  # type: ignore[assignment]
    list_display = (
        "pk",
        "email",
        "username",
        "first_name",
        "last_name",
        "is_staff",
    )
    list_filter = (
        "email",
        "is_staff",
        "is_active",
    )
    # list_editable = ("first_name",)
    # list_display_links = ("email",)
    # list_filter = ('pub_date',)
    search_fields = ("email", "username")
    ordering = ("email",)
    empty_value_display = _("empty")


admin.site.register(CustomUser, CustomUserAdmin)
