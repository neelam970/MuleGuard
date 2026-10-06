from django.urls import path

from .views import (
    AlertListCreateAPIView,
    AlertDetailAPIView,
    alert_page,
    alert_detail_page,
)

urlpatterns = [
    path(
        "",
        AlertListCreateAPIView.as_view(),
        name="alert-list-create",
    ),

    path(
        "page/",
        alert_page,
        name="alert-page",
    ),

    path(
        "<int:pk>/",
        AlertDetailAPIView.as_view(),
        name="alert-detail",
    ),
    path(
    "page/<int:pk>/",
    alert_detail_page,
    name="alert-detail-page",
),
]