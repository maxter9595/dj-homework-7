from django_filters import rest_framework as filters
from rest_framework.response import Response

from advertisements.models import Advertisement, AdvertisementStatusChoices


class AdvertisementFilter(filters.FilterSet):
    """
    Фильтры для объявлений
    """
    created_at_before = filters.DateFilter(
        field_name='created_at',
        lookup_expr='lte'
    )

    created_at_after = filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte'
    )

    creator = filters.NumberFilter(
        field_name='creator',
    )
    status = filters.ChoiceFilter(
        field_name='status',
        choices=AdvertisementStatusChoices.choices
    )

    class Meta:
        model = Advertisement
        fields = [
            'created_at_before',
            'created_at_after',
            'creator',
            'status'
        ]

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(
            queryset
        )
        user = self.request.user
        status = self.request.query_params.get(
            'status'
        )
        if status:
            if status == 'DRAFT':
                if user.is_authenticated:
                    return queryset.filter(
                        status='DRAFT',
                        creator=user
                    )
                else:
                    return Response(
                        {"error": "User is not authenticated"},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
        elif self.request.method == 'PATCH':
            new_status = self.request.data.get('status')
            if new_status in ['OPEN', 'CLOSE']:
                queryset.update(status=new_status)
                return queryset.filter(
                    status=new_status
                )
        return queryset.exclude(
            status='DRAFT'
        )
