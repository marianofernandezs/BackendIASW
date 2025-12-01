from django.db import models
from django.contrib.auth.models import User

class PaymentMethod(models.Model):
    """
    Modelo para almacenar un método de pago tokenizado de un usuario.
    Cumple con PCI al no almacenar datos sensibles de la tarjeta.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payment_methods',
        verbose_name='Usuario'
    )
    # Token generado por la pasarela de pago, representa el método de pago.
    token = models.CharField(
        max_length=255,
        unique=True, # Un token debe ser único en el sistema
        db_index=True,
        verbose_name='Token de pago'
    )
    # Metadatos de la tarjeta, útiles para mostrar al usuario.
    brand = models.CharField(
        max_length=50,
        verbose_name='Marca de tarjeta'
    ) # Ej: Visa, Mastercard
    last_four_digits = models.CharField(
        max_length=4,
        verbose_name='Últimos 4 dígitos'
    )
    expiry_month = models.IntegerField(
        verbose_name='Mes de expiración'
    )
    expiry_year = models.IntegerField(
        verbose_name='Año de expiración'
    )
    # Indica si el usuario dio consentimiento explícito para guardar la tarjeta.
    consent_given = models.BooleanField(
        default=False,
        verbose_name='Consentimiento otorgado'
    )
    # Indica si este es el método de pago predeterminado del usuario.
    is_default = models.BooleanField(
        default=False,
        verbose_name='Es predeterminado'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Última actualización'
    )

    class Meta:
        verbose_name = 'Método de Pago'
        verbose_name_plural = 'Métodos de Pago'
        # Asegura que un usuario no pueda tener dos métodos de pago con el mismo token
        # aunque el campo token ya es unique=True globalmente.
        # Esto previene errores lógicos si se cambia unique=True en el futuro.
        unique_together = ('user', 'token')

    def __str__(self):
        return f"{self.brand} ****{self.last_four_digits} (Exp: {self.expiry_month}/{self.expiry_year}) por {self.user.username}"

