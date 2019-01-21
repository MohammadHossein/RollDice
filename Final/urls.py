from django.urls import path

from Final.views import HomePage, CreateGame, GameView, RateAPI, BestGameAddedAPI, GamePlayedCountAPI, \
    AcceptGameComment, AcceptUserComment, EndGameAPI, GameCommentAPI, UserCommentAPI,UserProfile

urlpatterns = [
    path('', HomePage.as_view(), name='homepage'),
    path('create_game', CreateGame.as_view(), name='create_game'),
    path('game', GameView.as_view(), name='game_view'),
    path('game_rate', RateAPI.as_view(), name='game-rate'),
    path('best_game', BestGameAddedAPI.as_view(), name='best-game'),
    path('game_played', GamePlayedCountAPI.as_view(), name='game-rate'),
    path('game_comment', GameCommentAPI.as_view(), name='game-comment'),
    path('user_comment', UserCommentAPI.as_view(), name='user-comment'),
    path('accept_game_comment', AcceptGameComment.as_view(), name='accept-game-comment'),
    path('accept_user_comment', AcceptUserComment.as_view(), name='accept-user-comment'),
    path('end_game', EndGameAPI.as_view(), name='end_game'),
    path('profile', UserProfile.as_view(), name='profile'),
    # path('profile/<str:username>', temp, name='end_game'),
]
