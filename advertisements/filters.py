from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """
    FilterSet для объявлений
    created_at - фильтр по диапазону дат создания объявлений
    creator - фильтр по создателю объявления
    """
    created_at = filters.DateFromToRangeFilter(
    )
    creator = filters.ModelChoiceFilter(
        queryset=get_user_model().objects.all()
    )

    class Meta:
        model = Advertisement
        fields = [
            'created_at',
            'creator',
            'status'
        ]
