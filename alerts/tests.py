from decimal import Decimal
from datetime import datetime, timezone

from django.test import TestCase

from customers.models import Customer
from transactions.models import Transaction

from .models import Alert
from .services import create_alert_from_detection


class AlertServiceTest(TestCase):

    def setUp(self):

        self.sender = Customer.objects.create(
            customer_id="ALERT001",
            full_name="Alert Sender",
            email="alertsender@test.com",
            phone="9999999991",
            date_of_birth="1995-01-01",
            address="Test Address",
        )

        self.receiver = Customer.objects.create(
            customer_id="ALERT002",
            full_name="Alert Receiver",
            email="alertreceiver@test.com",
            phone="9999999992",
            date_of_birth="1995-01-01",
            address="Test Address",
        )

        self.transaction = Transaction.objects.create(
            transaction_id="ALERT-TXN-001",
            sender=self.sender,
            receiver=self.receiver,
            amount=Decimal("800000"),
            transaction_type="CREDIT",
            transaction_date=datetime(
                2026,
                10,
                5,
                10,
                0,
                tzinfo=timezone.utc,
            ),
            status="COMPLETED",
        )

    def test_alert_is_created_from_detection(self):

        detection_result = {
            "transaction_id": "ALERT-TXN-001",
            "is_suspicious": True,
            "risk_score": 30,
            "rules": [
                {
                    "rule": "HIGH_VALUE_TRANSACTION",
                    "is_suspicious": True,
                    "risk_score": 30,
                    "message": "Transaction exceeds high-value threshold.",
                },
                {
                    "rule": "MULTIPLE_SENDERS",
                    "is_suspicious": False,
                    "risk_score": 0,
                    "message": "Only one sender found.",
                },
            ],
        }

        alerts = create_alert_from_detection(
            self.transaction,
            detection_result,
        )

        self.assertEqual(len(alerts), 1)

        alert = alerts[0]

        self.assertEqual(
            alert.rule,
            "HIGH_VALUE_TRANSACTION",
        )

        self.assertEqual(
            alert.risk_score,
            30,
        )

        self.assertEqual(
            alert.severity,
            "MEDIUM",
        )

        self.assertEqual(
            alert.status,
            "OPEN",
        )

        self.assertEqual(
            alert.transaction,
            self.transaction,
        )

    def test_no_alert_created_for_normal_transaction(self):

        detection_result = {
            "transaction_id": "ALERT-TXN-001",
            "is_suspicious": False,
            "risk_score": 0,
            "rules": [
                {
                    "rule": "HIGH_VALUE_TRANSACTION",
                    "is_suspicious": False,
                    "risk_score": 0,
                    "message": "Transaction is normal.",
                },
            ],
        }

        alerts = create_alert_from_detection(
            self.transaction,
            detection_result,
        )

        self.assertIsNone(alerts)

        self.assertEqual(
            Alert.objects.count(),
            0,
        )