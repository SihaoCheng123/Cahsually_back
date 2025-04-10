from rest_framework import serializers
from datetime import datetime, time
from accounts.models import Account
from income.models import Income
from decimal import Decimal

class IncomeSerializer(serializers.ModelSerializer):
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), required=True)
    account_name = serializers.CharField(source='account.name', read_only=True)
    class Meta:
        model = Income
        fields = '__all__'
        extra_fields = ["account__name"]

    @staticmethod
    def validate_balance(value):
        if value <= Decimal('0.00'):
            raise serializers.ValidationError("Positive balance only")
        return value

    def validate(self, data):
        concept = data.get('concept')
        amount = data.get('amount')
        account = data.get('account')
        if not concept or not amount or not account:
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