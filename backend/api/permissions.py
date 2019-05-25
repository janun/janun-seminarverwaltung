from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj) -> bool:
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsOwnerOrVerwalterOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:
        if request.user.has_verwalter_role:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class HasStaffRole(permissions.BasePermission):
    "Checks user.has_staff_role"

    def has_permission(self, request, view) -> bool:
        return request.user.has_staff_role


class HasVerwalterRole(permissions.BasePermission):
    "Checks user has Verwalter Role"

    def has_permission(self, request, view) -> bool:
        return request.user.has_verwalter_role


class HasVerwalterRoleOrReadOnly(permissions.BasePermission):
    "Allow read operations, else check for Verwalter Role"

    def has_permission(self, request, view) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.has_verwalter_role


class HasStaffRoleOrReadOnly(permissions.BasePermission):
    "Allow read operations, else check for Staff Roles"

    def has_permission(self, request, view) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.has_staff_role


class IsReviewed(permissions.BasePermission):
    "Check for user.is_reviewed"

    def has_permission(self, request, view) -> bool:
        return request.user.is_reviewed
