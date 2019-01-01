from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from Code.urls import onlineUsers
from User.models import User
from User.permissions import IsAuthenticated
from User.serializers import UserLoginSerializer, UserRegisterSerializer


class Login(ObtainAuthToken):
    authentication_classes = ()

    @staticmethod
    def get(request):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(request, username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=User.objects.get(username=username))
            response = HttpResponseRedirect(redirect_to=reverse('test'))
            response.set_cookie('token', token.key, 65435, 3000, '/')
            return response
        else:
            return Response({'message': 'login failed!'}, status=status.HTTP_401_UNAUTHORIZED)


class LogOut(APIView):
    @staticmethod
    def get(request):
        try:
            Token.objects.get(user=request.user).delete()
            onlineUsers.remove(request.user)
            return Response({'message': 'You have successfully logged out!'})
        except:
            return Response({'message': 'Error Logout'})


class SignUp(APIView):
    authentication_classes = ()

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return HttpResponseRedirect(redirect_to=reverse('login'))

