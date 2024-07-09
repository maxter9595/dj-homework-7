from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    Класс для проверки прав админов и пользователей
    на создание, обновление и удаление объявлений
    """
    def has_object_permission(self, request, view, obj):
        """
        Выводит резрешение/запрет на создание, обновление и удаление объявлений
        """
        user = request.user
        return user and user.is_authenticated and (user.is_staff or obj.creator == user)


class IsOwnerPermission(BasePermission):
    """
    Класс для проверки прав на
    добавление объекта в избранное
    """
    def has_object_permission(self, request, view, obj):
        """
        Проверяет, что создатель объекта не соответствует
        пользователю, отправившему запрос
        """
        return obj.creator != request.user
