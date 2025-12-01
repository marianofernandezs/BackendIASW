from django.shortcuts import get_object_or_404
from tracking.models import Order, OrderLocation


class TrackingService:
    """
    Lógica de negocio para el seguimiento de pedidos en tiempo real (MVP).
    """

    def get_order_tracking_info(self, order_id: str) -> Order:
        """
        Obtiene el pedido solicitado, incluyendo su ubicación actual (OrderLocation).
        """
        return get_object_or_404(Order.objects.select_related("location"), order_id=order_id)

    def update_order_location(self, order_id: str, latitude: float, longitude: float) -> OrderLocation:
        """
        Actualiza (o crea) la ubicación del pedido.
        Esta es la pieza clave para el tracking real del MVP.
        """
        order = get_object_or_404(Order, order_id=order_id)

        # Obtiene o crea registro de ubicación del pedido
        location, _ = OrderLocation.objects.update_or_create(
            order=order,
            defaults={
                "latitude": latitude,
                "longitude": longitude,
            }
        )

        return location

    def mark_order_as_delivered(self, order_id: str) -> Order:
        """
        Marca el pedido como entregado.
        (Opcional para fines de tracking.)
        """
        order = get_object_or_404(Order, order_id=order_id)
        if order.status != 'DELIVERED':
            order.status = 'DELIVERED'
            order.save()
        return order
