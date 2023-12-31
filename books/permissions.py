from rest_framework import permissions

class IsadminOrStaffReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user.is_staff or request.user.is_superuser


class IscommentOwnerorReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS):
            return True
        return request.user == obj.owner