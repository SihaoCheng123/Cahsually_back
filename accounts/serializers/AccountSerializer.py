from decimal import Decimal

from rest_framework import serializers

from accounts.models import Account
from users.models import CustomUser


class AccountSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=True)
    class Meta:
        model = Account
        fields = '__all__'

    @staticmethod
    def validate_balance(value):
        if value <= Decimal('0.00'):
            raise serializers.ValidationError("Positive balance only")
        return value

    def validate(self, data):
        name = data.get('name')
        balance = data.get('balance')
        user = data.get('users')

        if not name or not balance or not user:
            raise serializers.ValidationError('Fields required')
        return data