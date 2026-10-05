from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):

    context = {
        "total_customers": 0,
        "total_transactions": 0,
        "risk_alerts": 0,
        "open_cases": 0,
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )