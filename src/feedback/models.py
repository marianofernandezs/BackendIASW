from django.db import models
from django.utils import timezone
import uuid


class Order(models.Model):
    """
    Representa un pedido que puede ser calificado.
    Este modelo es un stub temporal hasta que exista la app real de pedidos.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    delivery_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de Entrega"
    )

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f"Pedido {self.id}"


class DeliveryRating(models.Model):
    """
    Representa la calificación de satisfacción de una entrega.
    """

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='delivery_rating',
        verbose_name="Pedido"
    )

    score = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        verbose_name="Puntuación (1-5)"
    )

    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name="Comentarios"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )

    class Meta:
        verbose_name = "Calificación de Entrega"
        verbose_name_plural = "Calificaciones de Entrega"
        constraints = [
            models.UniqueConstraint(
                fields=['order'],
                name='unique_delivery_rating_per_order'
            )
        ]

    def __str__(self):
        return f"Calificación para Pedido {self.order.id}: {self.score} estrellas"
