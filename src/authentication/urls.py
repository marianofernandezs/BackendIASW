from django.urls import path
from .views import (
    PasswordResetRequestView,
    PasswordResetSentView,
    PasswordResetConfirmView
)

app_name = "authentication"

urlpatterns = [
    path("password-reset/", PasswordResetRequestView.as_view(), name="password_reset_request"),
    path("password-reset/sent/", PasswordResetSentView.as_view(), name="password_reset_sent"),
    path("password-reset/confirm/<int:uid>/<str:token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password-reset/complete/", PasswordResetSentView.as_view(), name="password_reset_complete"),
]
