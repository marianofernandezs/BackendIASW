from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from payment_methods.services import PaymentMethodService
from payment_methods.forms import PaymentMethodConsentForm
from payment_methods.serializers import PaymentMethodSerializer, PaymentMethodSaveSerializer
from payment_methods.models import PaymentMethod


class PaymentMethodListView(LoginRequiredMixin, View):
    """
    Vista para listar los métodos de pago guardados por el usuario.
    Requiere que el usuario esté autenticado.
    """
    template_name = 'payment_methods/list.html' # Asume la existencia de esta plantilla
    payment_method_service = PaymentMethodService()
    login_url = reverse_lazy('auth_management:login')

    def get(self, request, *args, **kwargs):
        """
        Muestra la lista de métodos de pago del usuario actual.
        """
        payment_methods = self.payment_method_service.get_user_payment_methods(request.user)
        return render(request, self.template_name, {'payment_methods': payment_methods})


class PaymentMethodDeleteView(LoginRequiredMixin, View):
    """
    Vista para manejar la eliminación de un método de pago.
    Requiere que el usuario esté autenticado.
    """
    payment_method_service = PaymentMethodService()
    login_url = reverse_lazy('auth_management:login')

    def post(self, request, pk, *args, **kwargs):
        """
        Elimina el método de pago especificado por PK para el usuario actual.
        """
        if self.payment_method_service.delete_payment_method(request.user, pk):
            messages.success(request, "Método de pago eliminado exitosamente.")
        else:
            messages.error(request, "No se pudo eliminar el método de pago o no existe.")
        return redirect(reverse_lazy('payment_methods:list'))

class PaymentMethodSetDefaultView(LoginRequiredMixin, View):
    """
    Vista para establecer un método de pago como predeterminado.
    """
    payment_method_service = PaymentMethodService()
    login_url = reverse_lazy('auth_management:login')

    def post(self, request, pk, *args, **kwargs):
        """
        Establece el método de pago especificado por PK como predeterminado para el usuario actual.
        """
        payment_method = self.payment_method_service.set_default_payment_method(request.user, pk)
        if payment_method:
            messages.success(request, f"'{payment_method.brand} ****{payment_method.last_four_digits}' establecido como método predeterminado.")
        else:
            messages.error(request, "No se pudo establecer el método de pago como predeterminado.")
        return redirect(reverse_lazy('payment_methods:list'))


class PaymentMethodSaveAPIView(APIView):
    """
    API View para guardar un método de pago tokenizado después de un proceso de pago.
    Asume que el token y los metadatos de la tarjeta ya fueron obtenidos de una pasarela de pago.
    """
    permission_classes = [IsAuthenticated]
    payment_method_service = PaymentMethodService()

    def post(self, request, *args, **kwargs):
        """
        Recibe los datos del método de pago (token, metadatos, consentimiento) y lo guarda.
        """
        serializer = PaymentMethodSaveSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = request.user
            consent_given = data.pop('save_card', False)

            if consent_given:
                payment_method = self.payment_method_service.create_payment_method(
                    user=user,
                    token=data['token'],
                    brand=data['brand'],
                    last_four_digits=data['last_four_digits'],
                    expiry_month=data['expiry_month'],
                    expiry_year=data['expiry_year'],
                    consent_given=consent_given
                )
                if payment_method:
                    response_serializer = PaymentMethodSerializer(payment_method)
                    return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(
                        {"detail": "El método de pago ya existe para este usuario o no se pudo guardar."},
                        status=status.HTTP_200_OK # O 409 CONFLICT si se prefiere
                    )
            else:
                return Response(
                    {"detail": "Consentimiento para guardar la tarjeta no otorgado."},
                    status=status.HTTP_200_OK # O 204 No Content
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentMethodListAPIView(APIView):
    """
    API View para listar los métodos de pago guardados por el usuario actual.
    """
    permission_classes = [IsAuthenticated]
    payment_method_service = PaymentMethodService()

    def get(self, request, *args, **kwargs):
        """
        Retorna la lista de métodos de pago del usuario.
        """
        payment_methods = self.payment_method_service.get_user_payment_methods(request.user)
        serializer = PaymentMethodSerializer(payment_methods, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PaymentMethodDeleteAPIView(APIView):
    """
    API View para eliminar un método de pago específico.
    """
    permission_classes = [IsAuthenticated]
    payment_method_service = PaymentMethodService()

    def delete(self, request, pk, *args, **kwargs):
        """
        Elimina un método de pago por su ID.
        """
        if self.payment_method_service.delete_payment_method(request.user, pk):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"detail": "Método de pago no encontrado o no pertenece al usuario."},
            status=status.HTTP_404_NOT_FOUND
        )
