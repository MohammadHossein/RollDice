from django.urls import path

from Final.views import HomePage, CreateGame, GameView, RateAPI, BestGameAddedAPI, GamePlayedCountAPI

urlpatterns = [
    path('', HomePage.as_view(), name='homepage'),
    path('create_game/', CreateGame.as_view(), name='create_game'),
    path('game/', GameView.as_view(), name='game_view'),
    path('game_rate', RateAPI.as_view(), name='game-rate'),
    path('best_game', BestGameAddedAPI.as_view(), name='best-game'),
    path('game_played', GamePlayedCountAPI.as_view(), name='game-rate'),
]
