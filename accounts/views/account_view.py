from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, \
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_204_NO_CONTENT, HTTP_200_OK
from rest_framework.views import APIView

from accounts.models import Account
from accounts.serializers import AccountSerializer
from users.models import CustomUser


class CreateAccountView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, slug):

        data = request.data
        try:
            user = CustomUser.objects.get(slug=slug)
            data['users'] = user.id
            serializer = AccountSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"success": "Account created successfully", "data": serializer.data},
                    status=HTTP_201_CREATED
                )
            else:
                return Response(
                    {"error": "Error creating account", "data": serializer.errors},
                    status=HTTP_400_BAD_REQUEST
                )
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found", "data": None},
                status=HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": "Connection error", "data": f'error{e}'},
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )


class DeleteAccountView(APIView):
    permission_classes = [AllowAny]
    def delete(self, request, slug):
        try:
            account = Account.objects.get(slug=slug)
            account.delete()
            return Response(
                {"success": "Account successfully eliminated", "data": None},
                status=HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {"error": "Account not found", "data": f"{e}"},
                status=HTTP_404_NOT_FOUND
            )

class GetAccountsByUser(APIView):
    permission_classes = [AllowAny]
    def get(self, request, slug, HTTP_400_NOT_FOUND=None):

        try:
            user = CustomUser.objects.get(slug=slug)
            accounts = [{
                "name": account.name,
                "balance": account.balance
            }   for account in user.accounts.all()]

            return Response(
                {"success": "Accounts retrieved successfully", "data" : accounts},
                status=HTTP_200_OK
            )
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found", "data": None},
                status=HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": "Connection error", "data": f"{e}"},
                status=HTTP_400_NOT_FOUND
            )
