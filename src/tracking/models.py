from django.db import models
from django.utils import timezone


class DeliveryPerson(models.Model):
    """
    Representa a un repartidor del sistema.
    Puede tener múltiples pedidos asignados.
    """
    driver_id = models.CharField(max_length=100, unique=True, verbose_name="ID Repartidor")
    name = models.CharField(max_length=255, verbose_name="Nombre Completo")

    # Ubicación actual del repartidor (opcional para el MVP)
    current_latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Latitud Actual"
    )
    current_longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Longitud Actual"
    )
    last_updated = models.DateTimeField(
        null=True, blank=True, verbose_name="Última Actualización Ubicación"
    )

    class Meta:
        verbose_name = "Repartidor"
        verbose_name_plural = "Repartidores"

    def __str__(self):
        return f"Repartidor: {self.name} ({self.driver_id})"


class Order(models.Model):
    """
    Representa un pedido asociado a un repartidor.
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('IN_TRANSIT', 'En Tránsito'),
        ('DELIVERED', 'Entregado'),
        ('CANCELLED', 'Cancelado'),
    ]

    order_id = models.CharField(max_length=100, unique=True, verbose_name="ID Pedido")

    delivery_person = models.ForeignKey(
        DeliveryPerson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_orders',
        verbose_name="Repartidor Asignado"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING',
        verbose_name="Estado del Pedido"
    )

    delivery_address = models.CharField(max_length=255, verbose_name="Dirección de Entrega")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f"Pedido: {self.order_id} - Estado: {self.get_status_display()}"

    def is_in_transit(self):
        return self.status == 'IN_TRANSIT'

    def is_delivered(self):
        return self.status == 'DELIVERED'


class OrderLocation(models.Model):
    """
    Ubicación actual del pedido.
    MVP: solo guardamos la última ubicación, no un historial completo.
    """
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='location',
        verbose_name="Pedido"
    )
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Latitud")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Longitud")
    timestamp = models.DateTimeField(auto_now=True, verbose_name="Actualizado en")

    class Meta:
        verbose_name = "Ubicación de Pedido"
        verbose_name_plural = "Ubicaciones de Pedido"

    def __str__(self):
        return f"Ubicación Pedido {self.order.order_id} - ({self.latitude}, {self.longitude})"
