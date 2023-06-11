from django.urls import path, include
from loan_app.apps.loans.views import LoansApi, AdminView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"loans", LoansApi, basename="loans")

url_patterns = [
    path("", include(router.urls)),
    path("loans/update_loan", AdminView.as_view(), name="update-loan"),
]
