from rest_framework import permissions


class MePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_superuser
            or request.user.is_admin
            or (obj == request.user)
        )


class GlobalPermission(permissions.BasePermission):

    admin_actions = (['list', 'retrieve', 'update', 'partial_update'])
    admin_and_superuser_actions = (['create', 'destroy'])

    def has_permission(self, request, view):

        if view.action in self.admin_actions:
            return (
                request.user
                and request.user.is_authenticated
                and request.user.is_admin
            )

        if view.action in self.admin_and_superuser_actions:
            return (
                request.user
                and request.user.is_authenticated
                and (request.user.is_superuser or request.user.is_admin)
            )

        return False
