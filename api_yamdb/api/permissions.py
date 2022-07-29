from rest_framework import permissions


class AdminStaffOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        # Разрешить доступ, если запросы "безопасны"
        # или пользователь "сотрудник"
        return (request.user.is_admin
                or request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return (request.user.is_admin
                or request.user.is_staff)


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_admin
        if request.method in permissions.SAFE_METHODS:
            return True
        return False
