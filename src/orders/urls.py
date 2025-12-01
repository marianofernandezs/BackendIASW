from django.urls import path
from .views import DeliveryContactAPIView

urlpatterns = [
    path('orders/<int:order_id>/contact/', DeliveryContactAPIView.as_view(),
         name='order-delivery-contact'),
]
