from rest_framework.authtoken.models import Token
from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        cookie = request.COOKIES.get('token')
        try:
            Token.objects.get(key=cookie)
            return True
        except:
            return False

    def has_object_permission(self, request, view, obj):
        pass
