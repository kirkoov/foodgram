# from django.db import models
# from django.contrib.auth import get_user_model


# User = get_user_model()


# class RecipeQuerySet(models.QuerySet):
#     ...


# class Subscription(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name="subscribed_to",
#         verbose_name="Подписчик",
#     )
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name="subscribed_by",
#         verbose_name="Автор",
#     )

#     def __str__(self):
#         return f"Подписка {self.user} на {self.author}"
