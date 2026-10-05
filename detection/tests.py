from decimal import Decimal
from datetime import datetime, timezone, timedelta

from django.test import TestCase

from customers.models import Customer
from transactions.models import Transaction

from .services import (
    check_high_value_transaction,
    check_multiple_senders,
    run_detection_rules,
)


class DetectionTestCase(TestCase):

    def setUp(self):
        self.sender = Customer.objects.create(
            customer_id="TEST001",
            full_name="Test Sender",
            email="sender@test.com",
            phone="9999999999",
            date_of_birth="1995-01-01",
            address="Test Address",
        )

        self.receiver = Customer.objects.create(
            customer_id="TEST002",
            full_name="Test Receiver",
            email="receiver@test.com",
            phone="8888888888",
            date_of_birth="1995-01-01",
            address="Test Address",
        )

    # ---------------------------------------------------------
    # 1. HIGH VALUE TRANSACTION
    # ---------------------------------------------------------

    def test_high_value_transaction_is_detected(self):

        transaction = Transaction.objects.create(
            transaction_id="TEST-TXN-001",
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

        result = check_high_value_transaction(transaction)

        self.assertTrue(result["is_suspicious"])
        self.assertEqual(result["risk_score"], 30)

    # ---------------------------------------------------------
    # 2. NORMAL TRANSACTION
    # ---------------------------------------------------------

    def test_normal_transaction_is_not_detected(self):

        transaction = Transaction.objects.create(
            transaction_id="TEST-TXN-002",
            sender=self.sender,
            receiver=self.receiver,
            amount=Decimal("50000"),
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

        result = check_high_value_transaction(transaction)

        self.assertFalse(result["is_suspicious"])
        self.assertEqual(result["risk_score"], 0)

    # ---------------------------------------------------------
    # 3. DETECTION ENGINE - HIGH VALUE
    # ---------------------------------------------------------

    def test_detection_engine_high_value(self):

        transaction = Transaction.objects.create(
            transaction_id="TEST-TXN-003",
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

        result = run_detection_rules(transaction)

        self.assertTrue(result["is_suspicious"])
        self.assertEqual(result["risk_score"], 30)

        self.assertEqual(
            result["transaction_id"],
            "TEST-TXN-003",
        )

    # ---------------------------------------------------------
    # 4. MULTIPLE SENDERS
    # ---------------------------------------------------------

    def test_multiple_senders_are_detected(self):

        sender_2 = Customer.objects.create(
            customer_id="TEST003",
            full_name="Second Sender",
            email="sender2@test.com",
            phone="7777777777",
            date_of_birth="1995-01-01",
            address="Test Address",
        )

        sender_3 = Customer.objects.create(
            customer_id="TEST004",
            full_name="Third Sender",
            email="sender3@test.com",
            phone="6666666666",
            date_of_birth="1995-01-01",
            address="Test Address",
        )

        Transaction.objects.create(
            transaction_id="TEST-TXN-004",
            sender=self.sender,
            receiver=self.receiver,
            amount=Decimal("90000"),
            transaction_type="CREDIT",
            transaction_date=datetime(
                2026,
                10,
                5,
                9,
                0,
                tzinfo=timezone.utc,
            ),
            status="COMPLETED",
        )

        Transaction.objects.create(
            transaction_id="TEST-TXN-005",
            sender=sender_2,
            receiver=self.receiver,
            amount=Decimal("85000"),
            transaction_type="CREDIT",
            transaction_date=datetime(
                2026,
                10,
                5,
                9,
                30,
                tzinfo=timezone.utc,
            ),
            status="COMPLETED",
        )

        transaction_3 = Transaction.objects.create(
            transaction_id="TEST-TXN-006",
            sender=sender_3,
            receiver=self.receiver,
            amount=Decimal("95000"),
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

        result = check_multiple_senders(transaction_3)

        self.assertTrue(result["is_suspicious"])
        self.assertEqual(result["risk_score"], 25)

    # ---------------------------------------------------------
    # 5. ONLY TWO SENDERS
    # ---------------------------------------------------------

    def test_two_senders_are_not_detected(self):

        sender_2 = Customer.objects.create(
            customer_id="TEST005",
            full_name="Another Sender",
            email="sender5@test.com",
            phone="7777777776",
            date_of_birth="1995-01-01",
            address="Test Address",
        )

        Transaction.objects.create(
            transaction_id="TEST-TXN-007",
            sender=self.sender,
            receiver=self.receiver,
            amount=Decimal("90000"),
            transaction_type="CREDIT",
            transaction_date=datetime(
                2026,
                10,
                5,
                9,
                0,
                tzinfo=timezone.utc,
            ),
            status="COMPLETED",
        )

        transaction_2 = Transaction.objects.create(
            transaction_id="TEST-TXN-008",
            sender=sender_2,
            receiver=self.receiver,
            amount=Decimal("85000"),
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

        result = check_multiple_senders(transaction_2)

        self.assertFalse(result["is_suspicious"])
        self.assertEqual(result["risk_score"], 0)

    # ---------------------------------------------------------
    # 6. SENDERS OUTSIDE 24-HOUR WINDOW
    # ---------------------------------------------------------

    def test_multiple_senders_outside_time_window_are_not_detected(self):

        sender_2 = Customer.objects.create(
            customer_id="TEST006",
            full_name="Old Sender",
            email="sender6@test.com",
            phone="7777777775",
            date_of_birth="1995-01-01",
            address="Test Address",
        )

        sender_3 = Customer.objects.create(
            customer_id="TEST007",
            full_name="Another Old Sender",
            email="sender7@test.com",
            phone="7777777774",
            date_of_birth="1995-01-01",
            address="Test Address",
        )

        Transaction.objects.create(
            transaction_id="TEST-TXN-009",
            sender=self.sender,
            receiver=self.receiver,
            amount=Decimal("90000"),
            transaction_type="CREDIT",
            transaction_date=datetime(
                2026,
                10,
                3,
                8,
                0,
                tzinfo=timezone.utc,
            ),
            status="COMPLETED",
        )

        Transaction.objects.create(
            transaction_id="TEST-TXN-010",
            sender=sender_2,
            receiver=self.receiver,
            amount=Decimal("85000"),
            transaction_type="CREDIT",
            transaction_date=datetime(
                2026,
                10,
                3,
                9,
                0,
                tzinfo=timezone.utc,
            ),
            status="COMPLETED",
        )

        transaction_3 = Transaction.objects.create(
            transaction_id="TEST-TXN-011",
            sender=sender_3,
            receiver=self.receiver,
            amount=Decimal("95000"),
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

        result = check_multiple_senders(transaction_3)

        self.assertFalse(result["is_suspicious"])
        self.assertEqual(result["risk_score"], 0)

    # ---------------------------------------------------------
    # 7. FAILED TRANSACTIONS SHOULD NOT COUNT
    # ---------------------------------------------------------

    def test_failed_transactions_are_not_counted(self):

        sender_2 = Customer.objects.create(
            customer_id="TEST008",
            full_name="Failed Sender",
            email="sender8@test.com",
            phone="7777777773",
            date_of_birth="1995-01-01",
            address="Test Address",
        )

        sender_3 = Customer.objects.create(
            customer_id="TEST009",
            full_name="Failed Sender Two",
            email="sender9@test.com",
            phone="7777777772",
            date_of_birth="1995-01-01",
            address="Test Address",
        )

        Transaction.objects.create(
            transaction_id="TEST-TXN-012",
            sender=self.sender,
            receiver=self.receiver,
            amount=Decimal("90000"),
            transaction_type="CREDIT",
            transaction_date=datetime(
                2026,
                10,
                5,
                9,
                0,
                tzinfo=timezone.utc,
            ),
            status="COMPLETED",
        )

        Transaction.objects.create(
            transaction_id="TEST-TXN-013",
            sender=sender_2,
            receiver=self.receiver,
            amount=Decimal("85000"),
            transaction_type="CREDIT",
            transaction_date=datetime(
                2026,
                10,
                5,
                9,
                30,
                tzinfo=timezone.utc,
            ),
            status="FAILED",
        )

        transaction_3 = Transaction.objects.create(
            transaction_id="TEST-TXN-014",
            sender=sender_3,
            receiver=self.receiver,
            amount=Decimal("95000"),
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

        result = check_multiple_senders(transaction_3)

        self.assertFalse(result["is_suspicious"])
        self.assertEqual(result["risk_score"], 0)

    # ---------------------------------------------------------
    # 8. HIGH VALUE + MULTIPLE SENDERS
    # ---------------------------------------------------------

    def test_multiple_rules_increase_risk_score(self):

        sender_2 = Customer.objects.create(
            customer_id="TEST010",
            full_name="Risk Sender Two",
            email="sender10@test.com",
            phone="7777777771",
            date_of_birth="1995-01-01",
            address="Test Address",
        )

        sender_3 = Customer.objects.create(
            customer_id="TEST011",
            full_name="Risk Sender Three",
            email="sender11@test.com",
            phone="7777777770",
            date_of_birth="1995-01-01",
            address="Test Address",
        )

        Transaction.objects.create(
            transaction_id="TEST-TXN-015",
            sender=self.sender,
            receiver=self.receiver,
            amount=Decimal("90000"),
            transaction_type="CREDIT",
            transaction_date=datetime(
                2026,
                10,
                5,
                9,
                0,
                tzinfo=timezone.utc,
            ),
            status="COMPLETED",
        )

        Transaction.objects.create(
            transaction_id="TEST-TXN-016",
            sender=sender_2,
            receiver=self.receiver,
            amount=Decimal("85000"),
            transaction_type="CREDIT",
            transaction_date=datetime(
                2026,
                10,
                5,
                9,
                30,
                tzinfo=timezone.utc,
            ),
            status="COMPLETED",
        )

        transaction = Transaction.objects.create(
            transaction_id="TEST-TXN-017",
            sender=sender_3,
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

        result = run_detection_rules(transaction)

        self.assertTrue(result["is_suspicious"])
        self.assertEqual(result["risk_score"], 55)

    # ---------------------------------------------------------
    # 9. EXACT THRESHOLD
    # ---------------------------------------------------------

    def test_exact_high_value_threshold_is_not_detected(self):

        transaction = Transaction.objects.create(
            transaction_id="TEST-TXN-018",
            sender=self.sender,
            receiver=self.receiver,
            amount=Decimal("500000"),
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

        result = check_high_value_transaction(transaction)

        self.assertFalse(result["is_suspicious"])
        self.assertEqual(result["risk_score"], 0)

    # ---------------------------------------------------------
    # 10. BELOW HIGH VALUE THRESHOLD
    # ---------------------------------------------------------

    def test_transaction_just_below_high_value_threshold(self):

        transaction = Transaction.objects.create(
            transaction_id="TEST-TXN-019",
            sender=self.sender,
            receiver=self.receiver,
            amount=Decimal("499999"),
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

        result = check_high_value_transaction(transaction)

        self.assertFalse(result["is_suspicious"])
        self.assertEqual(result["risk_score"], 0)