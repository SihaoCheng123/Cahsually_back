from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import CustomUser
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'password': {"write_only": True}
        }

    @staticmethod
    def validate_email(value):
        if value.endswith(".ru"):
            raise serializers.ValidationError("No .ru domains allowed")
        return value

    @staticmethod
    def validate_phone(value):
        if value and not value.isdigit():
            raise serializers.ValidationError("Only numbers allowed in phone")
        return value

    @staticmethod
    def validate_password(value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value

    @staticmethod
    def validate_values(self, data):
        if "name" not in data or not data.get("name"):
            raise serializers.ValidationError({"name": "Name field is required"})
        if "email" not in data or not data.get("email"):
            raise serializers.ValidationError({"email": "Email field is required"})
        if "password" not in data or not data.get("password"):
            raise serializers.ValidationError({"password": "Password field is required"})
        return data

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)

        if password:
            user.password = make_password(password)

        user.save()
        return user