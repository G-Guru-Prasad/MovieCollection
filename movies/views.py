from rest_framework import permissions, status
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.core.cache import cache

import logging
logger = logging.getLogger(__name__)

def html_render(request):
    context = {"username":"Guru"}
    return render(request, "dashboard.html", context)

class RegisterUser(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(username=username, password=password)
        refresh = RefreshToken.for_user(user)
        
        return Response({'access_token': str(refresh.access_token),}, status=status.HTTP_201_CREATED)

class RequestCount(APIView):
    permission_classes = [permissions.IsAuthenticated,]

    def get(self, request):
        count = cache.get('request_count', 0)
        return Response({'request_count': count})

class ResetRequestCount(APIView):
    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request):
        count = cache.set('request_count', 0)
        return Response({"message":"request count reset successfully"})