from django import forms

class PaymentMethodConsentForm(forms.Form):
    """
    Formulario simple para que el usuario indique si desea guardar su tarjeta.
    """
    save_card = forms.BooleanField(
        label="Guardar esta tarjeta para futuras compras",
        required=False, # No es obligatorio, el usuario puede optar por no guardarla
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

