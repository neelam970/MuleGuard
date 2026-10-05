from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    list_display = (
        "transaction_id",
        "sender",
        "receiver",
        "amount",
        "transaction_type",
        "transaction_date",
        "status",
    )

    list_filter = (
        "transaction_type",
        "status",
        "transaction_date",
    )

    search_fields = (
        "transaction_id",
        "sender__customer_id",
        "sender__full_name",
        "receiver__customer_id",
        "receiver__full_name",
    )

    ordering = (
        "-transaction_date",
    )