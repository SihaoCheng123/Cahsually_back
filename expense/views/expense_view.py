from datetime import datetime

from django.db import transaction
from django.db.models import Sum
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, \
    HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import APIView

from accounts.models import Account
from accounts.serializers import AccountSerializer
from expense.models import Expense
from expense.serializers import ExpenseSerializer
from users.models import CustomUser


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

class GetExpenseListByMonthView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, slug):

        try:
            user = CustomUser.objects.get(slug=slug)

            today = datetime.today()
            current_month = today.month
            current_year = today.year

            expenses = Expense.objects.filter(
                account__users = user,
                date__month = current_month,
                date__year = current_year
            ).order_by('-date')

            total_expense = expenses.aggregate(total=Sum('amount'))['total'] or 0

            serializer = ExpenseSerializer(expenses, many=True)
            return Response(
                {"success": "Expense list retrieved by month",
                 "data": {
                     "total_expense" : total_expense,
                     "list" : serializer.data
                 }}
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