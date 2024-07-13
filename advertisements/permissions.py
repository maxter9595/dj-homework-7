from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    Класс для проверки аутентифицированного владельца/создателя объявления.
    В зависимости от результата проверки будет дано/не дано то или иное разрешение
    """
    def has_object_permission(self, request, view, obj):
        """
        Проверяем является ли пользователь создателем/владельцем объявления
        """
        return obj.creator == request.user
