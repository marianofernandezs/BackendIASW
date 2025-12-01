import uuid
from django.conf import settings
from django.urls import reverse
from .models import PaymentAttempt

class PaymentServiceError(Exception):
    """Excepción base para errores en el PaymentService."""
    pass

class SecureEnvironmentFailureError(PaymentServiceError):
    """Excepción para cuando falla la creación del entorno seguro."""
    pass

class PaymentService:
    """
    Servicio encargado de la lógica de negocio relacionada con los pagos.
    Incluye la inicialización del entorno seguro y la gestión del estado del pago.
    """

    def _simulate_gateway_initiation(self, attempt_id: int, amount: float) -> str:
        """
        Simula la interacción con una pasarela de pago externa para iniciar
        un entorno seguro. En un entorno real, esto haría una llamada API
        a la pasarela (ej. Stripe, PayPal) y recibiría una URL de redirección.
        """
        # Genera un ID externo ficticio para la pasarela
        external_id = f"pgw_{uuid.uuid4().hex}"
        
        # Genera una URL de retorno ficticia para la pasarela de pago
        # que apunta a nuestro endpoint de callback.
        # Asegúrate de que `request` esté disponible para generar URLs absolutas si es necesario
        # Para simplificar, usaremos una URL relativa al sitio, la pasarela debería usar una absoluta
        # de callback, la cual debería ser configurada en sus ajustes.
        callback_url = settings.HOST_URL + reverse('checkout:payment_callback', kwargs={'attempt_id': attempt_id})
        
        # URL de la pasarela de pago simulada. Aquí redirigiríamos al usuario.
        # En un caso real, la URL de la pasarela incluiría parámetros
        # como el monto, el ID de la transacción y la URL de retorno.
        secure_url = (
            f"https://secure-payment-gateway.com/pay?"
            f"session_id={external_id}&amount={amount}&currency=USD&"
            f"return_url={callback_url}&cancel_url = settings.HOST_URL + reverse('checkout:payment_failed', kwargs={'attempt_id': attempt_id})"
        )
        
        print(f"DEBUG: Simulated secure environment URL: {secure_url}")
        return secure_url, external_id

    def initiate_secure_payment(self, amount: float, order_id: str = None) -> tuple[str, PaymentAttempt]:
        """
        Inicia el proceso de pago, creando un registro de intento y
        obteniendo la URL para el entorno seguro de la pasarela de pago.

        :param amount: El monto total a pagar.
        :param order_id: El ID de la orden o carrito asociado.
        :return: Una tupla con la URL de redirección al entorno seguro y el objeto PaymentAttempt.
        :raises SecureEnvironmentFailureError: Si no se puede iniciar el entorno seguro.
        """
        # 1. Crear un registro de intento de pago en nuestra base de datos
        payment_attempt = PaymentAttempt.objects.create(
            order_id=order_id,
            amount=amount,
            currency='USD',  # Moneda por defecto, podría ser configurable
            status=PaymentAttempt.PaymentStatus.PENDING
        )

        try:
            # 2. Interactuar con la pasarela de pago para iniciar la transacción
            # Esto debería ser una llamada a una API externa.
            # Aquí lo simulamos.
            secure_url, external_id = self._simulate_gateway_initiation(payment_attempt.id, amount)
            
            payment_attempt.external_id = external_id
            payment_attempt.secure_environment_url = secure_url
            payment_attempt.save()

            return secure_url, payment_attempt
        except Exception as e:
            # Si hay un error al interactuar con la pasarela, actualizamos el estado
            payment_attempt.status = PaymentAttempt.PaymentStatus.FAILED
            payment_attempt.error_message = f"Error al iniciar entorno seguro: {str(e)}"
            payment_attempt.save()
            raise SecureEnvironmentFailureError(f"No se pudo iniciar el entorno seguro: {e}")

    def process_payment_callback(self, attempt_id: int, is_success: bool, external_data: dict = None) -> PaymentAttempt:
        """
        Procesa la respuesta (callback) de la pasarela de pago.
        Actualiza el estado del intento de pago según el resultado de la transacción.

        :param attempt_id: El ID de nuestro intento de pago.
        :param is_success: Booleano que indica si la pasarela reportó un éxito.
        :param external_data: Datos adicionales recibidos de la pasarela (ej. token, ID de referencia).
        :return: El objeto PaymentAttempt actualizado.
        :raises PaymentServiceError: Si el intento de pago no existe o hay un error en el procesamiento.
        """
        try:
            payment_attempt = PaymentAttempt.objects.get(id=attempt_id)
        except PaymentAttempt.DoesNotExist:
            raise PaymentServiceError(f"Intento de pago con ID {attempt_id} no encontrado.")

        if is_success:
            payment_attempt.status = PaymentAttempt.PaymentStatus.SUCCESS
            payment_attempt.error_message = None
            if external_data and 'external_id' in external_data:
                 payment_attempt.external_id = external_data['external_id']
        else:
            payment_attempt.status = PaymentAttempt.PaymentStatus.FAILED
            payment_attempt.error_message = external_data.get('error', 'Pago fallido sin mensaje específico.')

        payment_attempt.save()
        return payment_attempt

# Configuración necesaria para simular la URL de host para callbacks.
# Esto se debería configurar en settings.py para un entorno real.
if not hasattr(settings, 'HOST_URL'):
    settings.HOST_URL = "http://127.0.0.1:8000" # URL base para la app local.
