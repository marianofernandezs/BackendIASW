from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from .forms import PaymentInitiationForm
from .models import PaymentAttempt
from .services import PaymentService, SecureEnvironmentFailureError, PaymentServiceError


class InitiatePaymentView(View):
    """
    Muestra el formulario de pago y delega la creacion del pago seguro.
    """

    def get(self, request):
        form = PaymentInitiationForm()
        return render(request, "checkout/initiate_payment.html", {"form": form})

    def post(self, request):
        form = PaymentInitiationForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            order_id = form.cleaned_data.get("order_id")

            payment_service = PaymentService()
            try:
                secure_url, payment_attempt = payment_service.initiate_secure_payment(amount, order_id)
                messages.info(request, "Redirigiendo a un entorno seguro para completar su transaccion.")
                return redirect(secure_url)
            except SecureEnvironmentFailureError as e:
                messages.error(request, f"Error al iniciar el proceso de pago. Intente mas tarde. ({e})")
                return render(request, "checkout/payment_error.html", {"error_message": str(e)})
            except Exception:
                messages.error(request, "Ocurrio un error inesperado. Por favor, intentelo de nuevo.")
                return render(request, "checkout/payment_error.html", {"error_message": "Error inesperado"})

        messages.error(request, "Por favor, corrija los errores en el formulario.")
        return render(request, "checkout/initiate_payment.html", {"form": form})


class PaymentCallbackView(View):
    """
    Maneja la redireccion de la pasarela una vez que el usuario completa/cancela el pago.
    """

    def get(self, request, attempt_id):
        is_success = request.GET.get("status") == "success"
        error_message = request.GET.get("error_message")
        external_id = request.GET.get("session_id")
        external_data = {"error": error_message, "external_id": external_id}

        payment_service = PaymentService()
        try:
            payment_attempt = payment_service.process_payment_callback(attempt_id, is_success, external_data)
            if payment_attempt.status == PaymentAttempt.PaymentStatus.SUCCESS:
                messages.success(request, "Pago completado con exito. Gracias por su compra.")
                return redirect(reverse("checkout:payment_success", kwargs={"attempt_id": payment_attempt.id}))

            messages.error(request, f"El pago no pudo completarse. {payment_attempt.error_message}")
            return redirect(reverse("checkout:payment_failed", kwargs={"attempt_id": payment_attempt.id}))

        except PaymentServiceError as e:
            messages.error(request, f"Error al procesar el resultado del pago. {e}")
            return redirect(reverse("checkout:payment_failed", kwargs={"attempt_id": attempt_id}))
        except Exception as e:
            messages.error(request, f"Ocurrio un error inesperado al procesar el callback. {e}")
            return redirect(reverse("checkout:payment_failed", kwargs={"attempt_id": attempt_id}))


class PaymentSuccessView(View):
    """Vista para mostrar un mensaje de exito despues de un pago."""

    def get(self, request, attempt_id):
        try:
            payment_attempt = PaymentAttempt.objects.get(id=attempt_id, status=PaymentAttempt.PaymentStatus.SUCCESS)
            return render(request, "checkout/payment_success.html", {"payment_attempt": payment_attempt})
        except PaymentAttempt.DoesNotExist:
            messages.error(request, "No se encontro un intento de pago exitoso con el ID proporcionado.")
            return redirect(reverse("checkout:initiate_payment"))


class PaymentFailedView(View):
    """Vista para mostrar un mensaje de fallo despues de un pago."""

    def get(self, request, attempt_id):
        try:
            payment_attempt = PaymentAttempt.objects.get(id=attempt_id)
            return render(request, "checkout/payment_failed.html", {"payment_attempt": payment_attempt})
        except PaymentAttempt.DoesNotExist:
            messages.error(request, "No se encontro un intento de pago con el ID proporcionado.")
            return redirect(reverse("checkout:initiate_payment"))


class PaymentErrorView(View):
    """Vista generica para errores de pago."""

    def get(self, request):
        error_message = request.GET.get("msg") or request.GET.get("error") or "Se produjo un error al procesar el pago."
        return render(request, "checkout/payment_error.html", {"error_message": error_message})
