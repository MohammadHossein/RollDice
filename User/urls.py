from django.urls import path

from User.views import Login, SignUp, Test,LogOut

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('logout/', LogOut.as_view(), name='logout'),
    path('test/', Test.as_view(), name='test')
]
