from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("customers/", views.customer_page, name="customer-page"),
    path(
        "customers/<int:pk>/investigate/",
        views.customer_investigate,
        name="customer-investigate",
    ),
]