from django.shortcuts import render
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from Code.urls import onlineUsers
from Final.models import Game
from Final.serializers import GameSerializer
from User.permissions import IsAuthenticated, Authenticate


class HomePage(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        return render(request, 'home.html', {'onlineUsers': onlineUsers, 'curUser': request.user})


class CreateGame(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (Authenticate,)

    @staticmethod
    def get(request):
        return render(request, 'game.html', {'onlineUsers': onlineUsers, 'curUser': request.user})

    @staticmethod
    def post(request):
        serializer = GameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        game = Game(**serializer.validated_data)
        game.user = request.user
        game.save()
        return Response('Done!')


class GameView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (Authenticate,)

    @staticmethod
    def get(request):
        return render(request, 'gameTemplate.html')
