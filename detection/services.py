from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from transactions.models import Transaction


def check_high_value_transaction(transaction):
    """
    Check whether a transaction exceeds
    the configured high-value threshold.
    """

    threshold = settings.HIGH_VALUE_TRANSACTION_THRESHOLD

    if transaction.amount > threshold:
        return {
            "rule": "HIGH_VALUE_TRANSACTION",
            "is_suspicious": True,
            "risk_score": 30,
            "message": (
                f"Transaction amount ₹{transaction.amount} "
                f"exceeds the high-value threshold "
                f"of ₹{threshold}."
            ),
        }

    return {
        "rule": "HIGH_VALUE_TRANSACTION",
        "is_suspicious": False,
        "risk_score": 0,
        "message": (
            "Transaction amount is within the normal threshold."
        ),
    }


def check_multiple_senders(transaction):
    """
    Check whether multiple unique customers
    sent money to the same receiver within
    the configured time window.
    """

    time_window = transaction.transaction_date - timedelta(
        hours=settings.MULTIPLE_SENDERS_TIME_WINDOW_HOURS
    )

    transactions = Transaction.objects.filter(
        receiver=transaction.receiver,
        transaction_date__gte=time_window,
        transaction_date__lte=transaction.transaction_date,
        status="COMPLETED",
    )

    unique_sender_count = (
        transactions
        .values("sender")
        .distinct()
        .count()
    )

    threshold = settings.MULTIPLE_SENDERS_THRESHOLD

    if unique_sender_count >= threshold:
        return {
            "rule": "MULTIPLE_SENDERS",
            "is_suspicious": True,
            "risk_score": 25,
            "message": (
                f"{unique_sender_count} different customers "
                f"sent money to "
                f"{transaction.receiver.full_name} "
                f"within "
                f"{settings.MULTIPLE_SENDERS_TIME_WINDOW_HOURS} hours."
            ),
        }

    return {
        "rule": "MULTIPLE_SENDERS",
        "is_suspicious": False,
        "risk_score": 0,
        "message": (
            f"Only {unique_sender_count} unique sender(s) "
            f"found within the configured time window."
        ),
    }


def run_detection_rules(transaction):
    """
    Run all detection rules for a transaction.
    """

    results = []

    # Rule 1: High-value transaction
    high_value_result = check_high_value_transaction(
        transaction
    )

    results.append(high_value_result)

    # Rule 2: Multiple senders
    multiple_senders_result = check_multiple_senders(
        transaction
    )

    results.append(multiple_senders_result)

    # Calculate total risk score
    total_risk_score = sum(
        result["risk_score"]
        for result in results
    )

    # Check whether any rule was triggered
    is_suspicious = any(
        result["is_suspicious"]
        for result in results
    )

    return {
        "transaction_id": transaction.transaction_id,
        "is_suspicious": is_suspicious,
        "risk_score": total_risk_score,
        "rules": results,
    }