"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("accounts.urls")),
    path("auth_management/", include("auth_management.urls")),
    path("authentication/", include("authentication.urls")),
    path("catalog/", include("catalog.urls")),
    path("feedback/", include("feedback.urls")),
    path("payments/", include("payments.urls")),
    path("checkout/", include("checkout.urls")),
    path("payment-methods/", include("payment_methods.urls")),
    # Alias to avoid 404s when login redirects to the default /accounts/login/
    path("accounts/login/", RedirectView.as_view(pattern_name="auth_management:login", permanent=False)),
]
