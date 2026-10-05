from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from customers.models import Customer
from transactions.models import Transaction


@login_required
def dashboard(request):

    total_customers = Customer.objects.count()
    total_transactions = Transaction.objects.count()

    context = {
        "total_customers": total_customers,
        "total_transactions": total_transactions,
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