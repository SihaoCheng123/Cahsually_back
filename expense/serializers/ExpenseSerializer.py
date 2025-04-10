from decimal import Decimal
from rest_framework import serializers
from datetime import datetime, time

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import APIView

from accounts.models import Account
from expense.models import Expense, CATEGORIES
from users.models import CustomUser


class ExpenseSerializer(serializers.ModelSerializer):
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), required=True)
    category = serializers.ChoiceField(choices=[(key, value) for key, value in CATEGORIES])
    account_name = serializers.CharField(source='account.name', read_only=True)
    class Meta:
        model = Expense
        fields = '__all__'
        extra_fields = ["account__name"]

    @staticmethod
    def validate_balance(value):
        if value <= Decimal('0.00'):
            raise serializers.ValidationError("Positive balance only")
        return value


    def validate_category(self, value):
        if value not in dict(CATEGORIES).keys():
            raise serializers.ValidationError("Invalid category")
        return value

    def validate(self, data):
        category = data.get('category')
        amount = data.get('amount')
        account = data.get('account')
        if not category or not amount or not account:
            raise serializers.ValidationError('Fields required')

        date = data.get('date')
        if isinstance(date, str):
            try:
                parsed_date = datetime.strptime(date, '%Y-%m-%d')
                date_with_time = datetime.combine(parsed_date.date(), time(hour=9, minute=0))
                data["date"] = date_with_time
            except:
                raise serializers.ValidationError("Invalid format for date")
        return data

class GetUserExpenseListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, slug):

        try:
            user = CustomUser.objects.get(slug=slug)
            expenses = Expense.objects.filter(account__users=user).order_by('-date')
            serializer = ExpenseSerializer(expenses, many=True)
            return Response(
                {"success": "Expense list retrieved successfully", "data": serializer.data},
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
