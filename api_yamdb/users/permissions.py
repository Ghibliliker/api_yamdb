from rest_framework import permissions


class IsRoleAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_admin
        )


class IsRoleAdminOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (request.user.is_superuser or request.user.is_admin)
        )
