from django.urls import path
from .views import LoginView, dashboard_view

app_name = "auth_management"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("dashboard/", dashboard_view, name="dashboard"),
]
