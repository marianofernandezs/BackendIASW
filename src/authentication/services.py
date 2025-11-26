import secrets
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings


class PasswordResetService:

    @staticmethod
    def generate_token(user):
        return default_token_generator.make_token(user)

    @staticmethod
    def send_reset_email(request, user):
        token = PasswordResetService.generate_token(user)
        reset_url = request.build_absolute_uri(
            reverse("authentication:password_reset_confirm", args=[user.pk, token])
        )

        subject = "Restablecimiento de contraseña"
        message = f"Hola, usa el siguiente enlace para restablecer tu contraseña:\n\n{reset_url}"

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return True

    @staticmethod
    def reset_password(user, new_password):
        user.set_password(new_password)
        user.save()
        return True
