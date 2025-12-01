import logging
import uuid

from django.db import models

logger = logging.getLogger("payments")


class PaymentTransactionManager(models.Manager):
    """Manager que acepta el alias transaction_id en consultas."""

    def _normalize_kwargs(self, kwargs):
        if "transaction_id" in kwargs:
            kwargs = kwargs.copy()
            kwargs["id"] = kwargs.pop("transaction_id")
        return kwargs

    def get(self, *args, **kwargs):
        kwargs = self._normalize_kwargs(kwargs)
        return super().get(*args, **kwargs)

    def filter(self, *args, **kwargs):
        kwargs = self._normalize_kwargs(kwargs)
        return super().filter(*args, **kwargs)


class PaymentTransaction(models.Model):
    """
    Stores payment attempts and their state.
    """

    class PaymentStatus(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        COMPLETED = "COMPLETED", "Completado"
        FAILED = "FAILED", "Fallido"
        REFUNDED = "REFUNDED", "Reembolsado"
        CANCELLED = "CANCELLED", "Cancelado"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=255, db_index=True, help_text="ID del usuario que realiza la compra")
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Monto total de la transaccion")
    currency = models.CharField(max_length=3, default="USD", help_text="Moneda de la transaccion (ej. 'USD', 'EUR')")
    status = models.CharField(
        max_length=10,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        help_text="Estado actual de la transaccion",
    )
    gateway_id = models.CharField(max_length=255, blank=True, null=True, help_text="ID de referencia de la pasarela de pago")
    gateway_response = models.JSONField(blank=True, null=True, help_text="Respuesta completa de la pasarela de pago")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Fecha y hora de creacion de la transaccion")
    updated_at = models.DateTimeField(auto_now=True, help_text="Fecha y hora de la ultima actualizacion de la transaccion")

    objects = PaymentTransactionManager()

    class Meta:
        verbose_name = "Transaccion de Pago"
        verbose_name_plural = "Transacciones de Pago"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Transaccion {self.id} - Usuario: {self.user_id} - Monto: {self.amount} {self.currency} - Estado: {self.status}"

    def save(self, *args, **kwargs):
        if self.pk and not self._state.adding and PaymentTransaction.objects.filter(pk=self.pk).exists():
            old_instance = PaymentTransaction.objects.get(pk=self.pk)
            if old_instance.status != self.status:
                logger.info("Transaction %s status change: '%s' -> '%s'", self.id, old_instance.status, self.status)
        super().save(*args, **kwargs)

    @property
    def transaction_id(self) -> str:
        return str(self.id)


class SavedPaymentMethod(models.Model):
    """
    Stores tokenized payment methods for users (requirement F9).
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=255, db_index=True, help_text="ID del usuario al que pertenece el metodo de pago")
    gateway_token = models.CharField(max_length=255, unique=True, help_text="Token seguro proporcionado por la pasarela de pago")
    card_brand = models.CharField(max_length=50, blank=True, null=True, help_text="Marca de la tarjeta (ej. 'Visa', 'Mastercard')")
    last_four_digits = models.CharField(max_length=4, blank=True, null=True, help_text="Ultimos cuatro digitos de la tarjeta")
    expiration_date = models.CharField(max_length=7, blank=True, null=True, help_text="Fecha de expiracion (MM/AAAA)")
    is_default = models.BooleanField(default=False, help_text="Indica si este es el metodo de pago por defecto del usuario")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Fecha y hora en que se guardo el metodo de pago")
    updated_at = models.DateTimeField(auto_now=True, help_text="Fecha y hora de la ultima actualizacion del metodo de pago")

    class Meta:
        verbose_name = "Metodo de Pago Guardado"
        verbose_name_plural = "Metodos de Pago Guardados"
        unique_together = ("user_id", "gateway_token")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Metodo de pago de {self.user_id} - {self.card_brand} ****{self.last_four_digits}"

    def save(self, *args, **kwargs):
        if self.is_default:
            SavedPaymentMethod.objects.filter(user_id=self.user_id).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)
