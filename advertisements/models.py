from django.db import models
from django.conf import settings


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


class Favorites(models.Model):
    """
    Избранные объявления
    user - пользователь, добавивший объявление в избранное
    favorites - объявление, добавленное в избранное
    created_at - дата добавления объявления в избранное
    updated_at - дата последнего изменения избранного объявления
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    favorites = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
