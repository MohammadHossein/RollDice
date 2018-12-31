from django.shortcuts import render

# Create your views here.
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from User.serializers import UserLoginSerializer


class Login(ObtainAuthToken):
    @staticmethod
    def get(request):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['username']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
        })

class Logout(APIView):
    pass


class SignUp(APIView):
    pass
