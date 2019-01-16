from django.http import HttpResponseRedirect
from rest_framework.authentication import BaseAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import exception_handler

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


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    # print(type(exc))
    if isinstance(exc, AuthenticationFailed) or isinstance(exc, PermissionDenied):
        return HttpResponseRedirect(redirect_to=reverse('login'))
    response = exception_handler(exc, context)

    #     custom_response_data = {
    #     'detail': 'This object does not exist.'  # custom exception message
    # }
    # response.data = custom_response_data  # set the custom response data on response object

    return response
