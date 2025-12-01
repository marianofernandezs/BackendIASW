from rest_framework import serializers
from tickets.models import Ticket, TicketStatusChoices

class TicketSerializer(serializers.ModelSerializer):
    """
    Serializador principal del Ticket.
    - 'status' es solo lectura para evitar que el cliente modifique estados.
    - La creación se delega al servicio.
    """
    status = serializers.ChoiceField(
        choices=TicketStatusChoices.choices,
        read_only=True,
        help_text="Estado del ticket: ABIERTO, EN_PROGRESO o CERRADO."
    )
    reporter_email = serializers.EmailField(
        required=False,
        allow_null=True,
        allow_blank=True
    )

    class Meta:
        model = Ticket
        fields = [
            'id',
            'ticket_number',
            'description',
            'status',
            'reporter_email',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'ticket_number',
            'status',
            'created_at',
            'updated_at'
        ]

    def create(self, validated_data):
        raise NotImplementedError("Usar TicketService para crear tickets.")

    def update(self, instance, validated_data):
        """
        Evita que el estado sea modificado por este serializer.
        """
        validated_data.pop('status', None)
        return super().update(instance, validated_data)


class TicketStatusUpdateSerializer(serializers.Serializer):
    """
    Serializer exclusivo para actualizar estado del ticket.
    """
    status = serializers.ChoiceField(
        choices=TicketStatusChoices.choices,
        help_text="Debe ser uno de: ABIERTO, EN_PROGRESO o CERRADO."
    )
