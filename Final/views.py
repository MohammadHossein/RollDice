import json
import random

from django.shortcuts import render
# Create your views here.
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from Code.urls import onlineUsers, games, non_started_games
from Final.models import Game, GameData
from Final.serializers import GameSerializer
from User.permissions import IsAuthenticated, Authenticate


class HomePage(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (Authenticate,)

    @staticmethod
    def get(request):
        return render(request, 'home.html', {'onlineUsers': onlineUsers, 'curUser': request.user,
                                             'games': Game.objects.all()})


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
            cur_game = non_started_games.pop()
            cur_game.turn = True
            return render(request, 'game_main.html',
                          {'game': game, 'game_id': cur_game.id, 'myTurn': 2})

        new_game = GameData(game.dice_count, game.max_score, [int(x) for x in game.hold.split(',')])
        games[new_game.id] = new_game
        non_started_games.append(new_game)
        return render(request, 'game_main.html', {'game': game, 'game_id': new_game.id, 'myTurn': 1})

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
