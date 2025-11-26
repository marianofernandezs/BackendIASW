from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.views import View

from .forms import LoginForm
from .services import AuthService

class LoginView(View):
    template_name = "auth_management/login.html"

    def get(self, request):
        return render(request, self.template_name, {"form": LoginForm()})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = AuthService.authenticate_user(email, password)

            if user:
                login(request, user)
                messages.success(request, "Sesión iniciada correctamente.")
                return redirect("auth_management:dashboard")

            messages.error(request, "Credenciales incorrectas.")

        return render(request, self.template_name, {"form": form})


def dashboard_view(request):
    return render(request, "auth_management/dashboard.html")
