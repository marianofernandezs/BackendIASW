from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.views import View

from .forms import PasswordResetRequestForm, PasswordResetConfirmForm
from .services import PasswordResetService


class PasswordResetRequestView(View):
    template_name = "authentication/password_reset_request.html"

    def get(self, request):
        return render(request, self.template_name, {"form": PasswordResetRequestForm()})

    def post(self, request):
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            user = User.objects.get(email=form.cleaned_data["email"])
            PasswordResetService.send_reset_email(request, user)
            return redirect("authentication:password_reset_sent")
        return render(request, self.template_name, {"form": form})


class PasswordResetSentView(View):
    template_name = "authentication/password_reset_sent.html"

    def get(self, request):
        return render(request, self.template_name)


class PasswordResetConfirmView(View):
    template_name = "authentication/password_reset_confirm.html"

    def get(self, request, uid, token):
        return render(request, self.template_name, {"form": PasswordResetConfirmForm()})

    def post(self, request, uid, token):
        user = User.objects.get(pk=uid)

        if not default_token_generator.check_token(user, token):
            return render(request, self.template_name, {"error": "El enlace es inválido o ha expirado."})

        form = PasswordResetConfirmForm(request.POST)
        if form.is_valid():
            PasswordResetService.reset_password(user, form.cleaned_data["new_password"])
            return redirect("auth_management:login")

        return render(request, self.template_name, {"form": form})
