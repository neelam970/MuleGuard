from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from customers.models import Customer


@login_required
def dashboard(request):

    total_customers = Customer.objects.count()

    context = {
        "total_customers": total_customers,
        "total_transactions": 0,
        "risk_alerts": 0,
        "open_cases": 0,
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )