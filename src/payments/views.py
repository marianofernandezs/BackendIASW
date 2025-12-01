import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, DestroyAPIView

from payments.serializers import (
    PaymentInitiationSerializer, PaymentConfirmationSerializer, SavedPaymentMethodSerializer
)
from payments.services import PaymentProcessor, MockPaymentGatewayService, PaymentMethodService
from payments.models import PaymentTransaction

logger = logging.getLogger('payments')

# Instanciamos los servicios con las dependencias
payment_gateway_service = MockPaymentGatewayService() # Usamos el mock para desarrollo/pruebas
payment_processor = PaymentProcessor(gateway_service=payment_gateway_service)
payment_method_service = PaymentMethodService()

class PaymentInitiateView(APIView):
    """
    Vista para iniciar un nuevo proceso de pago.
    Endpoint: POST /api/payments/initiate/
    """
    def post(self, request):
        serializer = PaymentInitiationSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            amount = serializer.validated_data['amount']
            currency = serializer.validated_data['currency']
            card_details = serializer.validated_data['card_details']
            save_method = serializer.validated_data.get('save_method', False)

            try:
                transaction = payment_processor.initiate_payment(user_id, amount, currency, card_details, save_method)
                return Response({
                    'transaction_id': transaction.id,
                    'status': transaction.status,
                    'message': 'Pago iniciado correctamente. Procesando...',
                    'gateway_id': transaction.gateway_id
                }, status=status.HTTP_202_ACCEPTED) # Accepted porque el pago puede tardar en confirmarse
            except Exception as e:
                logger.error(f"Error al iniciar pago para user {user_id}: {e}", exc_info=True)
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentConfirmView(APIView):
    """
    Vista para que las pasarelas de pago notifiquen el estado final de una transacción (webhook).
    Endpoint: POST /api/payments/confirm/
    """
    def post(self, request):
        serializer = PaymentConfirmationSerializer(data=request.data)
        if serializer.is_valid():
            transaction_id = serializer.validated_data['transaction_id']
            gateway_response = serializer.validated_data.get('gateway_response')
            status_param = serializer.validated_data['status']

            try:
                transaction = payment_processor.handle_gateway_callback(
                    transaction_id, gateway_response, status_param
                )
                return Response({
                    'transaction_id': transaction.id,
                    'status': transaction.status,
                    'message': 'Estado de transacción actualizado exitosamente.'
                }, status=status.HTTP_200_OK)
            except (PaymentTransaction.DoesNotExist, ValueError) as e:
                return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                logger.error(f"Error al confirmar pago para transacción {transaction_id}: {e}", exc_info=True)
                return Response({'error': 'Error interno del servidor al procesar la confirmación.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SavedPaymentMethodListView(ListAPIView):
    """
    Vista para listar los métodos de pago guardados de un usuario.
    Endpoint: GET /api/payments/saved_methods/<str:user_id>/
    """
    serializer_class = SavedPaymentMethodSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return payment_method_service.get_saved_methods(user_id)

class SavedPaymentMethodDetailView(DestroyAPIView):
    """
    Vista para eliminar un método de pago guardado.
    Endpoint: DELETE /api/payments/saved_methods/<uuid:pk>/
    """
    serializer_class = SavedPaymentMethodSerializer
    lookup_field = 'pk' # La clave primaria para buscar
    lookup_url_kwarg = 'method_id' # Nombre del argumento en la URL

    def get_queryset(self):
        # Asegurarse de que el usuario solo pueda eliminar sus propios métodos
        # Para este ejemplo, user_id se obtiene directamente del request o autenticación
        # Aquí asumimos que el user_id está en algún lugar del request, ej. request.user.id o un header
        # Para MVP, usaremos un user_id fijo o pasado por algún medio
        # Idealmente, esto se manejaría con autenticación de Django REST Framework.
        # Por ahora, se asume que un user_id real se pasaría y validaría.
        # Aquí, por simplicidad para el MVP sin AUTH, se requiere que se pase el user_id en la vista (DELETE).
        # Lo más seguro es que el usuario autenticado solo vea/elimine sus propios métodos.
        # Refactorizar: El servicio ya tiene user_id, se puede pasar al delete_method
        return payment_method_service.get_saved_methods(user_id="default_user") # TODO: Reemplazar con user_id real de autenticación

    def delete(self, request, *args, **kwargs):
        method_id = self.kwargs.get(self.lookup_url_kwarg)
        # TODO: Obtener user_id del request.user o de un token de autenticación
        # Por ahora, usamos un placeholder.
        user_id = request.headers.get('X-User-ID', 'anonymous_user') # Placeholder para user_id
        
        if payment_method_service.delete_method(method_id, user_id):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Método de pago no encontrado o no autorizado.'}, status=status.HTTP_404_NOT_FOUND)
