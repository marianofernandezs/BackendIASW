from django.urls import path
from tracking.views import (
    OrderTrackingAPIView,
    OrderLocationUpdateAPIView,
    tracking_demo_view
)

urlpatterns = [
    # Cliente consulta la ubicación de su pedido
    path('orders/<str:order_id>/', OrderTrackingAPIView.as_view(), name='order-tracking'),

    # Actualizar ubicación del pedido (simulado por repartidor o backend)
    path('orders/<str:order_id>/update/', OrderLocationUpdateAPIView.as_view(), name='order-location-update'),
    path("demo/", tracking_demo_view, name="tracking-demo"),

]
