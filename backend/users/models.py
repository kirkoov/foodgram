from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from backend.constants import (NUM_CHARS_EMAIL, NUM_CHARS_FIRSTNAME,
                               NUM_CHARS_LASTNAME)


class UserManager(BaseUserManager):
    """Use to be able to ID users based on their email vs username."""

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


class User(AbstractUser):
    """Use a custom user class, to make an email vs username difference."""

    email = models.EmailField(
        max_length=NUM_CHARS_EMAIL,
        unique=True,
        verbose_name=_("email"),
        help_text=_("Enter the preferred email here"),
    )
    first_name = models.CharField(
        max_length=NUM_CHARS_FIRSTNAME,
        verbose_name=_("first name"),
    )
    last_name = models.CharField(
        max_length=NUM_CHARS_LASTNAME,
        verbose_name=_("last name"),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username"]

    objects = UserManager()  # type: ignore[assignment, misc]

    class Meta:
        ordering = ("email",)
        verbose_name = _("custom user")
        verbose_name_plural = _("custom users")
        constraints = [
            models.UniqueConstraint(
                fields=["username", "email"], name="unique_username_email"
            )
        ]

    def __str__(self):
        return self.username


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="is_subscriber",
        verbose_name=_("subscriber"),
        help_text=_("Who subscribes"),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="is_subscribed",
        verbose_name=_("subscribed author"),
        help_text=_("which recipe author"),
    )

    class Meta:
        verbose_name = _("subscription")
        verbose_name_plural = _("subscriptions")
        constraints = [
            models.UniqueConstraint(
                fields=["user", "author"], name="unique_user_author_subscribe"
            ),
            models.CheckConstraint(
                check=~models.Q(author=models.F("user")),
                name="user_cannot_subscribe_to_themselves",
            ),
        ]

    def __str__(self):
        return f"{self.user}:{self.author}"
