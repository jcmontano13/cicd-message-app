# chat/views.py
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .models import UserProfile
import json


class RegisterView(APIView):
    def post(self, request):

        # --- Normalize request data for JSON, form-data, and Vercel wrapper ---
        content_type = request.content_type or ""

        if "_content" in request.POST:
            try:
                request_data = json.loads(request.POST["_content"])
            except json.JSONDecodeError:
                request_data = {}
        elif "application/x-www-form-urlencoded" in content_type or \
             "multipart/form-data" in content_type:
            request_data = request.POST
        else:
            request_data = request.data

        username = request_data.get("username")
        email = request_data.get("email")
        password = request_data.get("password")

        if not username or not password:
            return Response(
                {"error": "username and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        UserProfile.objects.create(user=user)

        return Response(
            {"message": "Registration successful"},
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    def post(self, request):

        # --- Normalize request data (same logic as RegisterView) ---
        content_type = request.content_type or ""

        if "_content" in request.POST:
            try:
                request_data = json.loads(request.POST["_content"])
            except json.JSONDecodeError:
                request_data = {}
        elif "application/x-www-form-urlencoded" in content_type or \
             "multipart/form-data" in content_type:
            request_data = request.POST
        else:
            request_data = request.data

        username = request_data.get("username")
        password = request_data.get("password")

        if not username or not password:
            return Response(
                {"error": "username and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {"error": "Invalid username or password"},
                status=status.HTTP_400_BAD_REQUEST
            )

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "user_id": user.id,
            "username": user.username
        })



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Logged out successfully"}, status=200)