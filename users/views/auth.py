from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR, \
    HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import CustomUser
from users.serializers import UserSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        email = data.get("email")

        if CustomUser.objects.filter(email=email).exists():
            return Response(
                {"error": "This email is in use already", "data" : None},
                status=HTTP_400_BAD_REQUEST)

        try:
            is_active = data.get("is_active", True)
            is_staff = data.get("is_staff", False)
            is_superuser = data.get("is_superuser", False)
            age = data.get("age")
            data["is_active"] = is_active
            data["is_staff"] = is_staff
            data["is_superuser"] = is_superuser
            data["age"] = age

            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"success": "User created successfully", "data": serializer.data},
                    status=HTTP_201_CREATED
                )
            else:
                return Response(
                    {"error": "Error creating user", "data": serializer.errors},
                    status=HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {"error": "Connection error", "data": f'error{e}'},
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

class DeleteUserView(APIView):
    permission_classes = [AllowAny]
    def delete(self, request, slug):
        try:
            user = CustomUser.objects.get(slug=slug)
            user.delete()
            return Response(
                {"success": "User deleted successfully", "data" : None},
                status=HTTP_204_NO_CONTENT
            )
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found", "data": None},
                status=HTTP_404_NOT_FOUND
            )

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')

        try:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)

                user_data = UserSerializer(user).data
                token = RefreshToken.for_user(user)
                user_data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
                return Response(
                    {"success": "Login successful", "data": user_data},
                    status=HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "Invalid credentials", "data": None},
                    status=HTTP_400_BAD_REQUEST
                )

        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found", "data": None},
                status=HTTP_404_NOT_FOUND
            )
