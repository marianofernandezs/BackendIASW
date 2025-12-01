from rest_framework import serializers
from tracking.models import Order, OrderLocation


class OrderLocationSerializer(serializers.ModelSerializer):
    """Serializa la ubicación actual del pedido."""

    class Meta:
        model = OrderLocation
        fields = ['latitude', 'longitude', 'timestamp']


class OrderTrackingSerializer(serializers.ModelSerializer):
    """
    Serializador principal de tracking.
    Devuelve la ubicación del pedido si existe.
    """
    location = OrderLocationSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['order_id', 'status', 'location']


class OrderLocationUpdateSerializer(serializers.Serializer):
    """
    Serializador para actualizar la ubicación del pedido.
    Ideal para el repartidor o el backend interno.
    """
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)
