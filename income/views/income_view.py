from django.db import transaction
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, \
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK
from rest_framework.views import APIView

from accounts.models import Account
from accounts.serializers import AccountSerializer
from income.models import Income
from income.serializers.IncomeSerializer import IncomeSerializer
from users.models import CustomUser


class CreateIncomeView(APIView):
    permission_classes = [AllowAny]
    @transaction.atomic
    def post(self, request, slug):

        try:
            account = Account.objects.get(slug=slug)
        except Exception as e:
            return Response(
                {"error": "Account not found", "data": None},
                status=HTTP_404_NOT_FOUND
            )

        try:
            data = request.data
            data["account"] = account.id

            serializer = IncomeSerializer(data=data)

            if serializer.is_valid():
                account.balance += serializer.validated_data["amount"]
                account.save()
                serializer.save()
                account_data = AccountSerializer(account).data
                return Response(
                    {"Success": "Income saved successfully", "data": account_data},
                    status=HTTP_201_CREATED
                )
            else:
                return Response(
                    {"error": "Error saving income", "data": serializer.errors},
                    status=HTTP_400_BAD_REQUEST
                )
        except Exception as e:
             return Response(
                {"error": "Connection error", "data": f'error{e}'},
                  status=HTTP_500_INTERNAL_SERVER_ERROR
             )

class GetUserIncomeListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, slug):

        try:
            user = CustomUser.objects.get(slug=slug)
            incomes = Income.objects.filter(account__users=user).order_by('-date')
            serializer = IncomeSerializer(incomes, many=True)
            return Response(
                {"success": "Income list retrieved successfully", "data": serializer.data},
                status=HTTP_200_OK
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