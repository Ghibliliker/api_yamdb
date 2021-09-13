from rest_framework import permissions


class IsRoleAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_admin
        )


class IsRoleModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_moderator
        )


class IsRoleAdminOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (request.user.is_superuser or request.user.is_admin)
        )


class IsRoleSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_superuser
        )


class IsRoleAdminOrOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        # is_owner = obj.username == request.user.username
        return (
            (obj.username == request.user.username)
            or request.user.is_admin
        )


class IsRoleOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username


class IsRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.role
        )


class IsAuthorOrReadOnlyPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class IsAuthenticatedAndAuthor(permissions.BasePermission):
    message = "Изменение чужого контента запрещено!"

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
