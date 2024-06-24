from rest_framework import permissions
from users.models import ProfileModel


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        try:
            user = ProfileModel.objects.get(user_id=request.user.id)
        except ProfileModel.DoesNotExist:
            return False
        return user.rule
