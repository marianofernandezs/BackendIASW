import uuid
from django.db import transaction
from django.core.validators import validate_email
from tickets.models import Ticket, TicketStatusChoices

class NotificationService:
    """
    Mock de servicio de notificaciones para eventos de tickets.
    """
    @staticmethod
    def send_ticket_resolved_notification(ticket: Ticket):
        if ticket.reporter_email:
            print(
                f"NOTIFICACIÓN → {ticket.reporter_email}: "
                f"Su ticket {ticket.ticket_number} ha sido CERRADO. "
                f"Descripción: '{ticket.description[:50]}...'"
            )
        else:
            print(f"NOTIFICACIÓN: Ticket {ticket.ticket_number} cerrado (sin email).")

class TicketService:
    """
    Lógica de negocio del ciclo de vida del ticket.
    """

    def __init__(self, notification_service=None):
        self.notification_service = notification_service or NotificationService()

    @staticmethod
    def generate_unique_ticket_number():
        return str(uuid.uuid4()).replace('-', '')[:12].upper()

    @transaction.atomic
    def create_ticket(self, description: str, reporter_email: str = None) -> Ticket:
        """
        Crea ticket con estado inicial ABIERTO.
        """
        if reporter_email:
            validate_email(reporter_email)

        ticket = Ticket.objects.create(
            ticket_number=self.generate_unique_ticket_number(),
            description=description,
            reporter_email=reporter_email,
            status=TicketStatusChoices.ABIERTO
        )
        return ticket

    @transaction.atomic
    def update_ticket_status(self, ticket: Ticket, new_status: str) -> Ticket:
        """
        Actualiza estado. Si pasa a CERRADO, se envía notificación.
        """
        if new_status not in TicketStatusChoices.values:
            raise ValueError(f"Estado '{new_status}' no válido.")

        if new_status == TicketStatusChoices.CERRADO:
            return self.close_ticket(ticket)

        ticket.status = new_status
        ticket.save()
        return ticket

    @transaction.atomic
    def close_ticket(self, ticket: Ticket) -> Ticket:
        """
        Cierra ticket y notifica.
        """
        if ticket.status == TicketStatusChoices.CERRADO:
            return ticket

        ticket.status = TicketStatusChoices.CERRADO
        ticket.save()
        self.notification_service.send_ticket_resolved_notification(ticket)
        return ticket
