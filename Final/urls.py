from django.urls import path

from Final.views import HomePage

urlpatterns = [
    path('', HomePage.as_view(), name='homepage')
]
