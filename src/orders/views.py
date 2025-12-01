from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from tracking.models import Order
from .serializers import DeliveryContactSerializer


class DeliveryContactAPIView(APIView):
    """
    HU10 — Devuelve el contacto del repartidor asignado al pedido.
    Solo el cliente dueño del pedido puede acceder.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)

        # 🔒 Validación de seguridad (muy importante)
        if order.customer != request.user:
            return Response({"detail": "No tienes permiso para ver este pedido."},
                            status=status.HTTP_403_FORBIDDEN)

        # No hay repartidor asignado aún
        if not order.delivery_person:
            return Response({"detail": "El pedido aún no tiene repartidor asignado."},
                            status=status.HTTP_404_NOT_FOUND)

        # Si el pedido NO está en reparto, no corresponde mostrar contacto
        if order.status != "IN_DELIVERY":
            return Response({"detail": "El repartidor solo está disponible cuando el pedido está en reparto."},
                            status=status.HTTP_400_BAD_REQUEST)

        user = order.delivery_person
        profile = getattr(user, "delivery_profile", None)

        if not profile:
            return Response({"detail": "El repartidor no tiene información de contacto disponible."},
                            status=status.HTTP_404_NOT_FOUND)

        # Serialización correcta
        serializer = DeliveryContactSerializer(profile, context={"user": user})
        return Response(serializer.data, status=status.HTTP_200_OK)
