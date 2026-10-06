from django.urls import path
from . import views
from transactions.views import transaction_page, transaction_detail
from alerts.views import alert_page, alert_detail_page
urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    path(
        "customers/",
        views.customer_page,
        name="customer-page",
    ),

    path(
        "customers/<int:pk>/investigate/",
        views.customer_investigate,
        name="customer-investigate",
    ),

    path(
        "transactions/",
        transaction_page,
        name="transaction-page",
    ),
path(
    "transactions/<int:pk>/",
    transaction_detail,
    name="transaction-detail",
),
path("alerts/", alert_page, name="alert-page"),
path(
    "alerts/<int:pk>/",
    alert_detail_page,
    name="alert-detail-page",
),
]