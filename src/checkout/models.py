from django.db import models

class PaymentAttempt(models.Model):
    """
    Modelo para registrar cada intento de pago.
    Permite rastrear el estado de una transacción y su asociación con una pasarela.
    """
    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pendiente'
        SUCCESS = 'SUCCESS', 'Éxito'
        FAILED = 'FAILED', 'Fallido'
        CANCELLED = 'CANCELLED', 'Cancelado'

    # Asocia con un usuario (puede ser null si el usuario no está autenticado)
    # from django.conf import settings
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, help_text="Usuario que inició el pago")

    # ID de referencia de la orden o carrito (simulado para este MVP)
    # En un sistema real, sería un ForeignKey a Order o Cart
    order_id = models.CharField(max_length=255, help_text="ID de la orden o carrito asociado", blank=True, null=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Monto del pago")
    currency = models.CharField(max_length=3, default='USD', help_text="Moneda del pago (ej. USD, EUR)")
    status = models.CharField(
        max_length=10,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        help_text="Estado actual del intento de pago"
    )
    external_id = models.CharField(max_length=255, blank=True, null=True, help_text="ID de transacción en la pasarela de pago")
    secure_environment_url = models.URLField(max_length=2000, blank=True, null=True, help_text="URL del entorno seguro de la pasarela de pago")
    error_message = models.TextField(blank=True, null=True, help_text="Mensaje de error si el pago falla")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Fecha y hora de creación del intento de pago")
    updated_at = models.DateTimeField(auto_now=True, help_text="Última fecha y hora de actualización del intento de pago")

    def __str__(self):
        """Representación en cadena del intento de pago."""
        return f"PaymentAttempt {self.id} for {self.amount} {self.currency} - Status: {self.status}"

    class Meta:
        verbose_name = "Intento de Pago"
        verbose_name_plural = "Intentos de Pago"
        ordering = ['-created_at']
