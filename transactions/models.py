from django.db import models

from customers.models import Customer


class Transaction(models.Model):

    TRANSACTION_TYPE_CHOICES = [
        ("CREDIT", "Credit"),
        ("DEBIT", "Debit"),
    ]

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
    ]

    transaction_id = models.CharField(
        max_length=30,
        unique=True
    )

    sender = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="sent_transactions"
    )

    receiver = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="received_transactions"
    )

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPE_CHOICES
    )

    transaction_date = models.DateTimeField()

    description = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="COMPLETED"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.transaction_id} - {self.amount}"