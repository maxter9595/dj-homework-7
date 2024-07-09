from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django_filters.rest_framework import DjangoFilterBackend

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, FavoriteAdvertisement
from advertisements.permissions import IsAdminOrReadOnly, IsOwnerPermission
from advertisements.serializers import AdvertisementSerializer, FavoriteAdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """
    ViewSet для объявлений
    """
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter
    filter_backends = [
        DjangoFilterBackend
    ]
    throttle_classes = [
        AnonRateThrottle,
        UserRateThrottle
    ]

    def create(self, request, *args, **kwargs):
        """
        - Создает новое объявление на основе данных запроса
        - Проверяет валидность данных, используя сериализатор
        """
        serializer = self.get_serializer(
            data=request.data
        )
        serializer.is_valid(
            raise_exception=True
        )
        self.perform_create(
            serializer
        )
        headers = self.get_success_headers(
            serializer.data
        )
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        """
        Вызывается для сохранения сериализатора
        после успешной валидации
        """
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        """
        - Обновляет часть данных существующего объявления
        - Проверяет права пользователя на обновление объявления
        """
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )
        serializer.is_valid(
            raise_exception=True
        )
        if request.user != instance.creator and not request.user.is_staff:
            raise ValidationError(
                "You are not allowed to update this advertisement."
            )
        self.perform_update(
            serializer
        )
        return Response(
            serializer.data
        )

    def destroy(self, request, *args, **kwargs):
        """
        - Удаляет существующее объявление
        - Проверяет права пользователя на удаление объявления
        """
        instance = self.get_object()
        if request.user != instance.creator and not request.user.is_staff:
            raise ValidationError(
                "You are not allowed to delete this advertisement."
            )
        instance.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(
            self.get_queryset()
        )
        serializer = self.get_serializer(
            queryset,
            many=True
        )
        return Response(
            serializer.data
        )

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsOwnerPermission]
    )
    def add_to_favorites(self, request, pk=None):
        """
        - Добавляет действие add_to_favorites для
          добавления объявления в избранные
        - Проверяет права пользователя на добавление
          объявления в избранное
        """
        advertisement = self.get_object()
        if advertisement.creator == request.user:
            raise ValidationError(
                "You cannot add your own advertisement to favorites."
            )
        favorite_advertisement, created = FavoriteAdvertisement.objects.get_or_create(
            user=request.user,
            advertisement=advertisement
        )
        if not created:
            raise ValidationError(
                "This advertisement is already in your favorites list."
            )
        serializer = FavoriteAdvertisementSerializer(
            favorite_advertisement
        )
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def favorite_advertisements(self, request):
        """
        - Позволяет получить список избранных объявлений
          для аутентифицированного пользователя
        - Проверяет, аутентифицирован ли пользователь, и
          возвращает список его избранных объявлений
        """
        if request.user.is_authenticated:
            user_favorites = FavoriteAdvertisement.objects.filter(
                user=self.request.user
            )
            advertisement_ids = user_favorites.values_list(
                'advertisement',
                flat=True
            )
            queryset = self.filter_queryset(
                self.get_queryset()
            )
            advertisements = queryset.filter(
                id__in=advertisement_ids
            )
            filterset = self.filterset_class(
                request.GET,
                queryset=advertisements
            )
            serializer = self.get_serializer(
                advertisements,
                many=True
            )
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "User is not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED
            )

    @action(
        detail=True,
        methods=['delete'],
        permission_classes=[IsOwnerPermission]
    )
    def remove_from_favorites(self, request, pk=None):
        """
        Позволяет удалить объявление из списка избранных
        """
        advertisement = self.get_object()
        favorite_advertisement = FavoriteAdvertisement.objects.filter(
            user=request.user,
            advertisement=advertisement
        ).first()
        if not favorite_advertisement:
            raise ValidationError(
                "This advertisement is not in your favorites list."
            )
        favorite_advertisement.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    def get_permissions(self):
        """
        Определяет права доступа
        """
        permission_actions = [
            "create",
            "update",
            "partial_update",
            "destroy"
        ]
        permission_classes = []
        if self.action in permission_actions:
            permission_classes += [
                IsAdminOrReadOnly
            ]
        return [
            permission() for permission in permission_classes
        ]
