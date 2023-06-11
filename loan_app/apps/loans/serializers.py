from django.core.exceptions import PermissionDenied

from rest_framework import serializers
from loan_app.apps.loans.models import Loan

import datetime


class LoansSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    amount = serializers.IntegerField()
    due_date = serializers.DateField()

    class Meta:
        model = Loan
        fields = (
            "id",
            "amount",
            "due_date",
            "status",
        )


class CreateLoanRequestSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    amount = serializers.IntegerField(required=True)
    duration_in_days = serializers.IntegerField(required=True)

    def create(self, validated_data):
        user = validated_data["user"]
        due_date = datetime.date.today() + datetime.timedelta(days=validated_data["duration_in_days"])
        loan = Loan.objects.create(
            amount=validated_data["amount"], user=user, due_date=due_date)
        return loan

    def validate(self, data):
        if data["user"].is_blocked:
            raise serializers.ValidationError("You are not allowed to request a loan.")
        return data

    def validate_amount(self, amount):
        if amount < 500 != 0:
            raise serializers.ValidationError("Amount must be greater than or equal to 500.")
        if amount % 500 != 0:
            raise serializers.ValidationError("Amount must be in multiples of 500.")
        return amount
        
        
    class Meta:
        model = Loan
        exclude = (
            "is_fully_paid", 
            "amount_paid",
            "due_date"
        )

class PayLoanRequestSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    amount = serializers.IntegerField(required=True)

    def update(self, instance, validated_data):
        user = validated_data["user"]
        if instance.user != user:
            raise PermissionDenied
        
        new_amount = instance.amount_paid + validated_data["amount"]
        instance.amount_paid = new_amount
        instance.save()
        return instance
        
    class Meta:
        model = Loan
        exclude = (
            "is_fully_paid", 
            "due_date"
        )

class UpdateLoanRequestSerializer(serializers.ModelSerializer):
    action = serializers.CharField(write_only=True)
    comment = serializers.CharField()
    
    amount = serializers.IntegerField(required=False)
    due_date = serializers.DateField(required=False)

    def update(self, instance, validated_data):
        action = validated_data.pop("action", None)
        comment = validated_data["comment"]

        if action == "APPROVE":
            instance.status = "APR"
        if action == "REJECT":
            instance.status = "REJ"
        instance.comment = comment
        instance.save()
        return instance
        
    def validate(self, data):
        if not data["comment"]:
            raise serializers.ValidationError("Please provide a comment.")
        if not data["action"]:
            raise serializers.ValidationError("Please provide an action.")
        return data

    class Meta:
        model = Loan
        fields = (
            "id", "amount", "due_date", "comment", "action"
        )
