from django.urls import path
from tickets.views import (
    TicketListCreateAPIView,
    TicketRetrieveAPIView,
    TicketStatusUpdateAPIView,
)

urlpatterns = [
    # Crear ticket + listar tickets
    path('', TicketListCreateAPIView.as_view(), name='ticket-list-create'),

    # Obtener un ticket específico
    path('<int:pk>/', TicketRetrieveAPIView.as_view(), name='ticket-detail'),

    # Actualizar estado del ticket
    path('<int:pk>/estado/', TicketStatusUpdateAPIView.as_view(), name='ticket-update-status'),
]
