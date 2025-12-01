from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.shortcuts import render


from tracking.services import TrackingService
from tracking.serializers import (
    OrderTrackingSerializer,
    OrderLocationUpdateSerializer
)
from tracking.models import Order


class OrderTrackingAPIView(APIView):
    """
    GET /tracking/<order_id>/
    Devuelve la ubicación actual del pedido.
    """
    service = TrackingService()

    def get(self, request, order_id):
        try:
            order = self.service.get_order_tracking_info(order_id)
            serializer = OrderTrackingSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"detail": "Pedido no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderLocationUpdateAPIView(APIView):
    """
    POST /tracking/<order_id>/update/
    Actualiza la ubicación del pedido (simulado por repartidor o sistema interno).
    """
    service = TrackingService()

    def post(self, request, order_id):
        serializer = OrderLocationUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            latitude = serializer.validated_data["latitude"]
            longitude = serializer.validated_data["longitude"]

            location = self.service.update_order_location(order_id, latitude, longitude)

            return Response(
                {
                    "message": "Ubicación del pedido actualizada correctamente.",
                    "location": {
                        "latitude": str(location.latitude),
                        "longitude": str(location.longitude),
                        "timestamp": location.timestamp,
                    },
                },
                status=status.HTTP_200_OK
            )
        except Order.DoesNotExist:
            return Response({"detail": "Pedido no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def tracking_demo_view(request):
    return render(request, "tracking/tracking.html")
