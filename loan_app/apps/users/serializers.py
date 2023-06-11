import re

from rest_framework import serializers
from django.core.validators import validate_email

from loan_app.apps.users.models import User


class UserValidateSerializer:
    @staticmethod
    def validate_name(value):
        if len(value) < 2:
            raise serializers.ValidationError(
                "Too short! It should at least 2 character long."
            )
        # No special characters allowed in name
        elif not bool(re.match("^[a-zA-Z ]*$", value)):
            raise serializers.ValidationError(
                "Special characters are not allowed in passenger name"
            )
        try:
            float(value)  # should not typecast to float
            raise serializers.ValidationError("This field can not be numeric.")
        except ValueError:
            pass  # good to go

    @staticmethod
    def validate_existing_email(email):
        email = email.lower()
        user = User.objects.filter(email=email)
        if not user:
            return email
        raise serializers.ValidationError(
            "This email address is already registered to an account."
        )


# class UserSerializer(serializers.Serializer):
class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        validators=[UserValidateSerializer.validate_name]
    )
    last_name = serializers.CharField(validators=[UserValidateSerializer.validate_name])
    email = serializers.CharField(
        validators=[validate_email, UserValidateSerializer.validate_existing_email]
    )
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        print("=====SERIALIZATION====")
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password",
        )


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
