from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages

from .forms import UserRegistrationForm
from .services import UserAccountService

class UserRegistrationView(View):
    """Vista para el registro de usuarios."""

    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts:registration_success")

    def get(self, request):
        return render(request, self.template_name, {"form": UserRegistrationForm()})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = UserAccountService.register_user(
                    email=form.cleaned_data["email"],
                    password=form.cleaned_data["password"],
                )
                messages.success(request, f"Cuenta creada para {user.email}")
                return redirect(self.success_url)
            except Exception as e:
                messages.error(request, f"Error inesperado: {e}")

        return render(request, self.template_name, {"form": form})
