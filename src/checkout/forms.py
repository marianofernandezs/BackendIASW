from django import forms

class PaymentInitiationForm(forms.Form):
    """
    Formulario para iniciar un proceso de pago.
    Recoge la información básica necesaria para un intento de pago.
    """
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        label="Monto a pagar",
        help_text="Introduce el monto total de la compra."
    )
    # Simulamos un order_id. En un sistema real, esto podría venir
    # de la sesión o ser un campo oculto asociado a un carrito preexistente.
    order_id = forms.CharField(
        max_length=255,
        required=False, # Podría ser requerido dependiendo de la lógica de negocio
        label="ID de la Orden",
        help_text="Referencia interna de la orden o carrito."
    )

    def clean_amount(self):
        """Valida que el monto sea un número positivo."""
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError("El monto debe ser un valor positivo.")
        return amount
