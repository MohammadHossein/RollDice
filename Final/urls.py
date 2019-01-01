from django.urls import path

from Final.views import HomePage, CreateGame, GameView

urlpatterns = [
    path('', HomePage.as_view(), name='homepage'),
    path('create_game/', CreateGame.as_view(), name='create_game'),
    path('game/', GameView.as_view(), name='game_view'),
]
