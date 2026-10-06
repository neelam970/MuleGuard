from django.contrib import admin

from .models import Alert


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = (
        "alert_id",
        "customer",
        "transaction",
        "rule",
        "risk_score",
        "severity",
        "status",
        "created_at",
    )

    list_filter = (
        "severity",
        "status",
        "rule",
    )

    search_fields = (
        "alert_id",
        "customer__customer_id",
        "customer__full_name",
        "transaction__transaction_id",
    )

    ordering = ("-created_at",)