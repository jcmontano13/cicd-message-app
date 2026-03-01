class RegisterView(APIView):
    def post(self, request):

        content_type = request.content_type or ""

        # --- Handle Vercel JSON-wrapped-as-form-data ---
        if "_content" in request.POST:
            import json
            try:
                request_data = json.loads(request.POST["_content"])
            except json.JSONDecodeError:
                request_data = {}
        # --- Normal form-data ---
        elif "application/x-www-form-urlencoded" in content_type or \
             "multipart/form-data" in content_type:
            request_data = request.POST
        # --- Normal JSON (local dev) ---
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