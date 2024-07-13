from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement, Favorites


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer для пользователей (берем из готовой модели User)
    """
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
        ]
        read_only_fields = [
            'id',
            'username',
            'first_name',
            'last_name',
        ]


class AdvertisementSerializer(serializers.ModelSerializer):
    """
    Serializer для объявлений
    """
    # Учет создателя объявления через UserSerializer
    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = [
            'id',
            'title',
            'description',
            'creator',
            'status',
            'created_at',
        ]

    def create(self, validated_data):
        """
        Создание объявления с учетом дополнительной логики
        (основная логика + учет информации о пользователе creator)
        """
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """
        Валидация данных при создании и
        обновлении открытых объявлений
        """
        if 'status' in data:
            if data['status'] == 'CLOSED':
                return data
        user_name = self.context['request'].user
        open_ads_number = Advertisement.objects.filter(
            creator=user_name,
            status='OPEN'
        ).count()
        if open_ads_number >= 10:
            raise ValidationError(
                'Превышено количество открытых объявлений'
            )
        else:
            return data


class FavoritesSerializer(serializers.ModelSerializer):
    """
    Serializer для избранных объявлений
    """
    # Учет объявления через AdvertisementSerializer
    favorites = AdvertisementSerializer(
        read_only=True,
    )

    class Meta:
        model = Favorites
        fields = [
            'id',
            'user',
            'favorites',
        ]
