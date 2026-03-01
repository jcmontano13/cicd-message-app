# chat/views.py
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile


class RegisterView(APIView):
    def post(self, request):

        # --- Handle both JSON and form-data safely ---
        content_type = request.content_type or ""

        if "application/x-www-form-urlencoded" in content_type:
            # Vercel-safe: form POST
            request_data = request.POST

        elif "multipart/form-data" in content_type:
            # Also safe: multipart
            request_data = request.POST

        else:
            # JSON or DRF-parsed body
            request_data = request.data

        # Extract fields
        username = request_data.get("username")
        email = request_data.get("email")
        password = request_data.get("password")

        # Validation
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

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Create profile
        UserProfile.objects.create(user=user)

        return Response(
            {"message": "Registration successful"},
            status=status.HTTP_201_CREATED
        )