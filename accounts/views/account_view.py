from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, \
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_204_NO_CONTENT, HTTP_200_OK
from rest_framework.views import APIView

from accounts.models import Account
from accounts.serializers import AccountSerializer
from expense.models import Expense
from expense.serializers import ExpenseSerializer
from income.models import Income
from income.serializers.IncomeSerializer import IncomeSerializer
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
    def get(self, request, slug):

        try:
            user = CustomUser.objects.get(slug=slug)
            accounts = [{
                "name": account.name,
                "balance": account.balance,
                "slug": account.slug
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
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

class GetOperationListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, slug):
        try:
            account = Account.objects.get(slug=slug)
        except:
            return Response(
                {"error": "Account not found", "data" : None},
                status=HTTP_404_NOT_FOUND
            )

        try:
            incomes = Income.objects.filter(account=account)
            expenses = Expense.objects.filter(account=account)

            operations = list(incomes) + list(expenses)

            operations.sort(key=lambda x: x.date, reverse=True)

            serialized_operations = []

            for operation in operations:
                if isinstance(operation, Income):
                    serialized_operations.append(IncomeSerializer(operation).data)
                else:
                    serialized_operations.append(ExpenseSerializer(operation).data)

            return Response(
                {"success": "Operation list successfully retrieved", "data": serialized_operations},
                status=HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": "Connection error", "data": f'error{e}'},
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )