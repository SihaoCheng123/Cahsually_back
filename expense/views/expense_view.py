from django.db import transaction
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, \
    HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import APIView

from accounts.models import Account
from accounts.serializers import AccountSerializer
from expense.serializers import ExpenseSerializer


class CreateExpenseView(APIView):
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
            serializer = ExpenseSerializer(data=data)
            if serializer.is_valid():
                account.balance -= serializer.validated_data["amount"]
                account.save()
                serializer.save()
                account_data = AccountSerializer(account).data
                return Response(
                    {"Success": "Expense saved successfully", "data": account_data},
                    status=HTTP_201_CREATED
                )
            else:
                return Response(
                    {"error": "Error saving expense", "data": serializer.errors},
                    status=HTTP_400_BAD_REQUEST
                )
        except Exception as e:
             return Response(
                {"error": "Connection error", "data": f'error{e}'},
                  status=HTTP_500_INTERNAL_SERVER_ERROR
             )