from django.urls import path

from User.views import Login

urlpatterns = [
    path('login/', Login.as_view())
]
