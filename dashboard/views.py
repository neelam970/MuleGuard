from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

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

def customer_page(request):
    return render(
        request,
        "customers/customers.html"
    )
def customer_investigate(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    return render(
        request,
        "customers/investigate.html",
        {"customer": customer}
    )