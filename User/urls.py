from django.urls import path

from User.views import Login, SignUp, Test

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('test/', Test.as_view(), name='test')
]
