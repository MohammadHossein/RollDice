from rest_framework.authentication import BaseAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import BasePermission

from Code.urls import onlineUsers
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
            user_id = Token.objects.get(key=cookie).user_id
            user = User.objects.get(id=user_id)
        # except User.DoesNotExist:
        #     raise AuthenticationFailed('No such user')
        except Exception:
            return None
        onlineUsers.add(user)
        return user, user.isAdmin
