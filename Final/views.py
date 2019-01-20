import json
import random

from django.http import HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from Code.urls import onlineUsers, games, non_started_games
from Final.models import Game, GameData, GameComment, UserComment
from Final.serializers import GameSerializer, GameRateSerializer, GamePlayedCountSerializer, GameCommentSerializer, \
    GameAcceptCommentSerializer, UserAcceptCommentSerializer, UserCommentSerializer
from User.permissions import IsAuthenticated, Authenticate


class HomePage(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (Authenticate,)

    @staticmethod
    def get(request):
        return render(request, 'home.html', {'onlineUsers': onlineUsers, 'curUser': request.user,
                                             'games': Game.objects.all(),
                                             'bestGame': Game.objects.values('rate', 'name').order_by('-rate')[0],
                                             'maxOnline': 0,
                                             'bestNewGame': Game.objects.all().order_by('-creation_date', '-rate')[0],
                                             'isAdmin': request.auth, 'user_comment': UserComment.objects.all(),
                                             'game_comment': GameComment.objects.all()})


class GameView(APIView):
    # permission_classes = (IsAuthenticated,)
    authentication_classes = (Authenticate,)

    @staticmethod
    def get(request: Request):
        game_id = request.query_params.get('id')
        # my_turn = request.query_params.get('p')
        if not game_id:
            return render(request, 'game_list.html')
            # raise NotFound('Game not found!')
        game = Game.objects.get(id=game_id)
        if not game:
            raise NotFound('Game not found!')
        if len(non_started_games) > 0:
            cur_game: GameData = non_started_games.pop()
            cur_game.turn = True
            cur_game.player2_id = request.user.id
            cur_game.started = True
            return render(request, 'game_main.html',
                          {'game': game, 'game_id': cur_game.id, 'myTurn': 2, 'myUserID': request.user.id})

        new_game = GameData(game.dice_count, game.max_score, [int(x) for x in game.hold.split(',')])
        new_game.player1_id = request.user.id
        games[new_game.id] = new_game
        non_started_games.append(new_game)
        return render(request, 'game_main.html',
                      {'game': game, 'game_id': new_game.id, 'myTurn': 1, 'myUserID': request.user.id})

    @staticmethod
    def post(request: Request):
        action = request.data.get('action')
        game_id = request.data.get('game_id')
        if not game_id:
            raise ValidationError('game_id not found')
        if not action:
            raise ValidationError('action not found')
        game: GameData = games.get(game_id)
        if not game:
            raise NotFound('game not found')
        if action == 'roll-dice':
            randoms = []
            change_turn = False
            for i in range(game.dice_count):
                rand = random.randrange(1, 7)
                change_turn = change_turn or (rand in game.hold)
                randoms.append(rand)
            if change_turn:
                game.turn = not game.turn
                game.player1_current = 0
                game.player2_current = 0
            game.dices = randoms
            if not change_turn:
                if game.turn:
                    game.player1_current += sum(randoms)
                else:
                    game.player2_current += sum(randoms)
        elif action == 'hold':
            game.player1_total += game.player1_current
            game.player1_current = 0
            game.player2_total += game.player2_current
            game.player2_current = 0
            game.turn = not game.turn
            if game.player1_total >= game.max_score:
                game.winner = True
            if game.player2_total >= game.max_score:
                game.winner = False
        return Response(json.dumps(game.__dict__))


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


class RateAPI(ListAPIView):
    serializer_class = GameRateSerializer
    model = Game

    def get_queryset(self):
        return Game.objects.values('rate', 'name')


class GamePlayedCountAPI(ListAPIView):
    serializer_class = GamePlayedCountSerializer
    model = Game

    def get_queryset(self):
        return Game.objects.values('play_count', 'name')


class BestGameAddedAPI(ListAPIView):
    serializer_class = GameSerializer
    model = Game

    def get_queryset(self):
        return Game.objects.all().order_by('creation_date', 'rate')


class GameCommentAPI(ListCreateAPIView):
    authentication_classes = (Authenticate,)
    serializer_class = GameCommentSerializer
    queryset = GameComment.objects.all()


class UserCommentAPI(ListCreateAPIView):
    authentication_classes = (Authenticate,)
    serializer_class = UserCommentSerializer
    queryset = UserComment.objects.all()


class AcceptGameComment(APIView):
    @staticmethod
    def post(request: Request):
        ser = GameAcceptCommentSerializer(data=request.data)
        ser.is_valid(True)
        vd = ser.validated_data
        GameComment.objects.filter(id__in=vd['game_comment']).update(accept=True)
        return HttpResponseRedirect(redirect_to=reverse('homepage'))


class AcceptUserComment(APIView):
    @staticmethod
    def post(request: Request):
        ser = UserAcceptCommentSerializer(data=request.data)
        ser.is_valid(True)
        vd = ser.validated_data
        UserComment.objects.filter(id__in=vd['user_comment']).update(accept=True)
        return HttpResponseRedirect(redirect_to=reverse('homepage'))


class EndGameAPI(APIView):
    @staticmethod
    def get(request: Request):
        non_started_games.pop()
        del games[request.query_params.get('id')]
        print(games)
        return Response("timeout")

    @staticmethod
    def post(request: Request):
        return Response()
