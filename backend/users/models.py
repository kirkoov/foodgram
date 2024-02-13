from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError("No required email set.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


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

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()  # type: ignore[assignment, misc]

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
