from django.contrib.auth.decorators import login_required
from rest_framework import status
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .filters import AdvertisementFilter
from .permissions import IsOwnerOrReadOnly
from .models import Advertisement, Favorites
from .serializers import AdvertisementSerializer, FavoritesSerializer


class AdvertisementViewSet(ModelViewSet):
    """
    ViewSet для объявлений
    """
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.request.user and self.request.user.is_staff:
            return [
                IsAuthenticated(),
            ]
        if self.action in ["update", "partial_update", "destroy"]:
            return [
                IsAuthenticated(),
                IsOwnerOrReadOnly(),
            ]
        return []

    def get_queryset(self):
        creator = self.request.query_params.get(
            'creator'
        )
        if creator:
            if int(creator) == self.request.user.id or self.request.user.is_staff:
                queryset = Advertisement.objects.filter(
                    creator=creator,
                )
            else:
                queryset = Advertisement.objects.filter(
                    creator=creator
                ).exclude(
                    status='DRAFT',
                )
            return queryset
        if self.request.user.is_staff:
            queryset = Advertisement.objects.all()
        else:
            queryset = Advertisement.objects.exclude(
                status='DRAFT'
            )
        return queryset

    @action(
        methods=['post', 'get'],
        detail=True,
    )
    def favorite(self, request, pk=None):
        if not bool(request.user and request.user.is_authenticated):
            return HttpResponse(
                'Неавторизованные пользователи не могут управлять избранным'
            )
        method = self.request.method
        user = self.request.user
        favorite = self.get_object()
        if method == 'POST':
            favorites = Favorites.objects.filter(
                user=user,
                favorites=favorite
            ).exists()
            if favorites:
                return HttpResponse(
                    'Объявление уже было добавлено в избранное'
                )
            elif user == favorite.creator:
                return HttpResponse(
                    'Вы не можете добавить свое объявление к себе в избранное'
                )
            else:
                Favorites.objects.create(
                    user=user,
                    favorites=favorite
                )
                return Response(
                    status=status.HTTP_201_CREATED
                )
        if method == 'GET':
            favorites = Favorites.objects.filter(
                favorites=favorite
            )
            serializer = FavoritesSerializer(
                favorites,
                many=True
            )
            return Response(
                serializer.data
            )

    @action(
        methods=['get'],
        detail=False,
    )
    def favorites(self, request):
        if not bool(request.user and request.user.is_authenticated):
            return HttpResponse(
                'Неавторизованные пользователи не могут управлять избранным'
            )
        user = self.request.user
        queryset = Favorites.objects.filter(
            user=user
        )
        serializer = FavoritesSerializer(
            queryset,
            many=True
        )
        return Response(
            serializer.data
        )
