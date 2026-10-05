from datetime import date

from rest_framework import serializers

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = "__all__"

    def validate_customer_id(self, value):
        value = value.strip().upper()

        if not value.startswith("CUST"):
            raise serializers.ValidationError(
                "Customer ID must start with CUST."
            )

        if len(value) > 20:
            raise serializers.ValidationError(
                "Customer ID cannot exceed 20 characters."
            )

        return value

    def validate_full_name(self, value):
        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "Full name must contain at least 3 characters."
            )

        if not all(char.isalpha() or char.isspace() for char in value):
            raise serializers.ValidationError(
                "Full name can contain only letters and spaces."
            )

        return value

    def validate_phone(self, value):
        value = value.strip()

        if not value.isdigit():
            raise serializers.ValidationError(
                "Phone number must contain only digits."
            )

        if len(value) != 10:
            raise serializers.ValidationError(
                "Phone number must contain exactly 10 digits."
            )

        return value

    def validate_date_of_birth(self, value):
        if value >= date.today():
            raise serializers.ValidationError(
                "Date of birth must be in the past."
            )

        return value

    def validate_address(self, value):
        value = value.strip()

        if len(value) < 5:
            raise serializers.ValidationError(
                "Address must contain at least 5 characters."
            )

        return value

    def validate(self, attrs):
        email = attrs.get("email")

        if email:
            attrs["email"] = email.strip().lower()

        return attrs