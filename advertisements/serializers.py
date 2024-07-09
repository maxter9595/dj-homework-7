from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement, FavoriteAdvertisement


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer для пользователей
    """
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
        )


class AdvertisementSerializer(serializers.ModelSerializer):
    """
    Serializer для объявлений
    """
    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = (
            'id',
            'title',
            'description',
            'creator',
            'status',
            'created_at',
        )

    def create(self, validated_data):
        """
        Используется для создания нового объявления
        """
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """
        Используется для валидации данных перед
        созданием или обновлением объявления
        """
        user = self.context.get(
            "request"
        ).user

        open_count = user.advertisement_set.filter(
            status='OPEN'
        ).count()

        if open_count >= 10:
            raise ValidationError(
                "User cannot have more than 10 open advertisements."
            )

        return data


class FavoriteAdvertisementSerializer(serializers.ModelSerializer):
    """
    Serializer для избранных объявлений
    """
    class Meta:
        model = FavoriteAdvertisement
        fields = '__all__'
