from .models import Alert


def get_alert_severity(risk_score):
    if risk_score >= 75:
        return "CRITICAL"

    if risk_score >= 50:
        return "HIGH"

    if risk_score >= 25:
        return "MEDIUM"

    return "LOW"


def create_alert_from_detection(transaction, detection_result):

    if not detection_result["is_suspicious"]:
        return None

    severity = get_alert_severity(
        detection_result["risk_score"]
    )

    alerts = []

    for rule_result in detection_result["rules"]:

        if not rule_result["is_suspicious"]:
            continue

        alert = Alert.objects.create(
            alert_id=f"ALT-{transaction.id}-{rule_result['rule']}",
            customer=transaction.receiver,
            transaction=transaction,
            rule=rule_result["rule"],
            risk_score=rule_result["risk_score"],
            severity=severity,
            message=rule_result["message"],
            status="OPEN",
        )

        alerts.append(alert)

    return alerts