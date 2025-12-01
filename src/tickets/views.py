from rest_framework.generics import ListCreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status

from tickets.models import Ticket
from tickets.serializers import (
    TicketSerializer,
    TicketStatusUpdateSerializer
)
from tickets.services import TicketService


class TicketListCreateAPIView(ListCreateAPIView):
    """
    HU14 — Crear Ticket:
    - GET → Lista todos los tickets.
    - POST → Crea un ticket con estado inicial ABIERTO.
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    service = TicketService()

    def perform_create(self, serializer):
        """
        La creación real ocurre en el servicio.
        """
        data = serializer.validated_data
        ticket = self.service.create_ticket(
            description=data.get("description"),
            reporter_email=data.get("reporter_email")
        )
        return ticket

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ticket = self.perform_create(serializer)
        output = TicketSerializer(ticket).data

        return Response(output, status=status.HTTP_201_CREATED)


class TicketRetrieveAPIView(RetrieveAPIView):
    """
    Obtener detalles de un ticket.
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class TicketStatusUpdateAPIView(UpdateAPIView):
    """
    Actualizar el estado del ticket:
    - Solo se usa TicketService.update_ticket_status()
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketStatusUpdateSerializer
    service = TicketService()

    def update(self, request, *args, **kwargs):
        ticket = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_status = serializer.validated_data["status"]
        updated_ticket = self.service.update_ticket_status(ticket, new_status)

        return Response(
            TicketSerializer(updated_ticket).data,
            status=status.HTTP_200_OK
        )
