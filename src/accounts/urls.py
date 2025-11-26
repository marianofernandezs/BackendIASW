from django.urls import path
from .views import UserRegistrationView
from django.views.generic import TemplateView

app_name = "accounts"

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),

    path(
        "register/success/",
        TemplateView.as_view(template_name="accounts/registration_success.html"),
        name="registration_success",
    )
]
