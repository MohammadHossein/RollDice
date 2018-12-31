from rest_framework.authentication import BaseAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission

from User.models import User


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


class Authenticate(BaseAuthentication):
    def authenticate(self, request):
        cookie = request.COOKIES.get('token')
        if not cookie:
            return None

        try:
            user = Token.objects.get(key=cookie).user
        except User.DoesNotExist:
            raise AuthenticationFailed('No such user')

        return (user, None)