from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "customer_id",
        "full_name",
        "email",
        "kyc_status",
        "risk_level",
        "account_status",
        "created_at",
    )

    list_filter = (
        "kyc_status",
        "risk_level",
        "account_status",
    )

    search_fields = (
        "customer_id",
        "full_name",
        "email",
        "phone",
    )