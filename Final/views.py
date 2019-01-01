from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView

from Code.urls import onlineUsers
from User.permissions import IsAuthenticated


class HomePage(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return render(request, 'index.html', {'onlineUsers': onlineUsers})
