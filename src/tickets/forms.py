from django import forms
from tickets.models import Ticket, TicketStatusChoices

class TicketCreationForm(forms.ModelForm):
    """
    Formulario para la creación de un nuevo ticket de soporte.
    """
    class Meta:
        model = Ticket
        fields = ['description', 'reporter_email']
        labels = {
            'description': 'Descripción del problema',
            'reporter_email': 'Tu correo electrónico (opcional)',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe tu problema aquí...'}),
            'reporter_email': forms.EmailInput(attrs={'placeholder': 'ejemplo@correo.com'}),
        }

class TicketStatusUpdateForm(forms.Form):
    """
    Formulario para actualizar el estado de un ticket.
    """
    status = forms.ChoiceField(
        choices=TicketStatusChoices.choices,
        label='Nuevo Estado del Ticket',
        help_text='Selecciona el nuevo estado para este ticket.'
    )

    def clean_status(self):
        """
        Valida que el estado seleccionado sea un valor permitido.
        """
        status = self.cleaned_data['status']
        if status not in TicketStatusChoices.values:
            raise forms.ValidationError("El estado seleccionado no es válido.")
        return status
