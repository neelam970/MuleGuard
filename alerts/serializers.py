from rest_framework import serializers

from .models import Alert


class AlertSerializer(serializers.ModelSerializer):

    customer_name = serializers.CharField(
        source="customer.full_name",
        read_only=True
    )

    customer_id = serializers.CharField(
        source="customer.customer_id",
        read_only=True
    )

    transaction_id = serializers.CharField(
        source="transaction.transaction_id",
        read_only=True
    )

    class Meta:
        model = Alert

        fields = [
            "id",
            "alert_id",
            "customer",
            "customer_id",
            "customer_name",
            "transaction",
            "transaction_id",
            "rule",
            "risk_score",
            "severity",
            "message",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "customer_id",
            "customer_name",
            "transaction_id",
            "created_at",
            "updated_at",
        ]