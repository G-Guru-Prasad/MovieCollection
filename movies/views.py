from rest_framework import permissions, status
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.core.cache import cache

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def html_render(request):
    context = {"username":"Guru"}
    print("Request came for dashboard rendering")
    return render(request, "dashboard.html", context)

class RegisterUser(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            print("User name and password is empty. username - {0} & password {1}".format(username, password))
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            print("Username already exists in database- {0}".format(username))
            return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create(username=username, password=password)
            refresh = RefreshToken.for_user(user)
        except Exception as e:
            print("Unable to create user table record for username - {0} and password - {1}".format(username, password))
            return Response({'error': 'Unable to create user.'}, status=status.HTTP_400_BAD_REQUEST)
        
        print("User - {0} successfully created".format(username))
        return Response({'access_token': str(refresh.access_token),}, status=status.HTTP_201_CREATED)

class RequestCount(APIView):
    permission_classes = [permissions.IsAuthenticated,]

    def get(self, request):
        count = cache.get('request_count', 0)
        print("Request count fetched from cache - {0}".format(count))
        return Response({'request_count': count})

class ResetRequestCount(APIView):
    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request):
        count = cache.set('request_count', 0)
        print("Request count resetted in cache")
        return Response({"message":"request count reset successfully"})