from django.utils import timezone
from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):

    sender_name = serializers.CharField(
        source="sender.full_name",
        read_only=True
    )

    sender_customer_id = serializers.CharField(
        source="sender.customer_id",
        read_only=True
    )

    receiver_name = serializers.CharField(
        source="receiver.full_name",
        read_only=True
    )

    receiver_customer_id = serializers.CharField(
        source="receiver.customer_id",
        read_only=True
    )

    class Meta:
        model = Transaction

        fields = [
            "id",
            "transaction_id",
            "sender",
            "sender_customer_id",
            "sender_name",
            "receiver",
            "receiver_customer_id",
            "receiver_name",
            "amount",
            "transaction_type",
            "transaction_date",
            "description",
            "status",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "sender_customer_id",
            "sender_name",
            "receiver_customer_id",
            "receiver_name",
        ]

    def validate_transaction_id(self, value):
        value = value.strip().upper()

        if not value:
            raise serializers.ValidationError(
                "Transaction ID is required."
            )

        if len(value) > 30:
            raise serializers.ValidationError(
                "Transaction ID cannot exceed 30 characters."
            )

        return value

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Transaction amount must be greater than 0."
            )

        return value

    def validate_transaction_date(self, value):
        if value > timezone.now():
            raise serializers.ValidationError(
                "Transaction date cannot be in the future."
            )

        return value

    def validate(self, attrs):

        sender = attrs.get("sender")
        receiver = attrs.get("receiver")

        # For PUT/PATCH, use the existing values if they
        # are not included in the request.
        if self.instance:
            sender = sender or self.instance.sender
            receiver = receiver or self.instance.receiver

        if sender and receiver and sender == receiver:
            raise serializers.ValidationError({
                "receiver": "Sender and receiver cannot be the same customer."
            })

        return attrs