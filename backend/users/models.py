from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """Use a custom user class to tweak more options later if needed."""

    email = models.EmailField(
        max_length=settings.NUM_CHARS_EMAIL,
        blank=False,
        unique=True,
        verbose_name=_("email"),
        help_text=_("Enter the preferred email here"),
    )
    first_name = models.CharField(
        max_length=settings.NUM_CHARS_FIRSTNAME,
        blank=False,
        verbose_name=_("first name"),
    )
    last_name = models.CharField(
        max_length=settings.NUM_CHARS_LASTNAME,
        blank=False,
        verbose_name=_("last name"),
    )

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    # REQUIRED_FIELDS = ["email"]

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["username", "email"], name="unique_username_email"
            )
        ]
        ordering = ("last_name", "first_name")
        verbose_name = _("custom user")
        verbose_name_plural = _("custom users")

    def __str__(self):
        return self.username
