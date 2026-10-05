from django.urls import path

from .views import (
    TransactionListCreateAPIView,
    TransactionDetailAPIView,
    transaction_page,
)


urlpatterns = [
    path(
        "",
        TransactionListCreateAPIView.as_view(),
        name="transaction-list-create",
    ),

    path(
        "<int:pk>/",
        TransactionDetailAPIView.as_view(),
        name="transaction-detail",
    ),

    path(
        "page/",
        transaction_page,
        name="transaction-page",
    ),
]