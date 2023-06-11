from django.urls import path
from loan_app.apps.users.views import CreateUserApiView, LoginUserAPIView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

url_patterns = [
    path("sign_up/", CreateUserApiView.as_view(), name="sign_up"),
    path("login/", LoginUserAPIView.as_view(), name="login"),
    path("refresh_token", TokenRefreshView.as_view(), name="token_refresh"),
]
