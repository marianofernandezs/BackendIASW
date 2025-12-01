from django.db import models
from django.utils.translation import gettext_lazy as _

class TicketStatusChoices(models.TextChoices):
    """
    Define los estados posibles para un ticket de soporte.
    """
    ABIERTO = 'ABIERTO', _('Abierto')
    EN_PROGRESO = 'EN_PROGRESO', _('En Progreso')
    CERRADO = 'CERRADO', _('Cerrado')

class Ticket(models.Model):
    """
    Modelo para representar un ticket de soporte.
    """
    ticket_number = models.CharField(
        max_length=20, 
        unique=True, 
        verbose_name=_("Número de Ticket"),
        help_text=_("Número único de seguimiento del ticket.")
    )
    description = models.TextField(verbose_name=_("Descripción de la Incidencia"))
    status = models.CharField(
        max_length=15,
        choices=TicketStatusChoices.choices,
        default=TicketStatusChoices.ABIERTO,
        verbose_name=_("Estado")
    )
    reporter_email = models.EmailField(
        blank=True, 
        null=True, 
        verbose_name=_("Email del Reportador"),
        help_text=_("Correo electrónico del cliente que reporta la incidencia.")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de Creación"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Última Actualización"))

    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")
        ordering = ['-created_at']

    def __str__(self):
        """Representación en cadena del objeto Ticket."""
        return f"Ticket {self.ticket_number} - {self.get_status_display()}"
