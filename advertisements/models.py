from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class AdvertisementStatusChoices(models.TextChoices):
    """
    Статусы объявлений
    OPEN - Открыто
    CLOSED - Закрыто
    DRAFT - Черновик
    """
    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"
    DRAFT = "DRAFT", "Черновик"


class Advertisement(models.Model):
    """
    Объявления
    title - заголовок объявления
    description - описание объявления
    status - статус объявления
    creator - автор объявления
    created_at - дата создания объявления
    updated_at - дата последнего изменения объявления
    """
    title = models.TextField(
    )
    description = models.TextField(
        default=''
    )
    status = models.TextField(
        choices=AdvertisementStatusChoices.choices,
        default=AdvertisementStatusChoices.OPEN
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )


class FavoriteAdvertisement(models.Model):
    """
    Избранные объявления
    user - пользователь, добавивший объявление в избранное
    advertisement - объявление, добавленное в избранное
    created_at - дата добавления объявления в избранное
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    advertisement = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
