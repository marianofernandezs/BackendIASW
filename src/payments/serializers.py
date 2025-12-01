from rest_framework import serializers
from payments.models import SavedPaymentMethod

class CardDetailsSerializer(serializers.Serializer):
    """
    Serializador para los detalles de la tarjeta de crédito.
    No se almacena raw data, solo se usa para validación de entrada.
    """
    card_number = serializers.CharField(max_length=16, min_length=13, help_text="Número de tarjeta de crédito (sin espacios)")
    expiry_month = serializers.CharField(max_length=2, help_text="Mes de expiración (MM)")
    expiry_year = serializers.CharField(max_length=4, help_text="Año de expiración (AAAA)")
    cvc = serializers.CharField(max_length=4, min_length=3, help_text="Código de seguridad de la tarjeta (CVC/CVV)")

    def validate(self, data):
        """
        Validación básica de la fecha de expiración.
        """
        # Aquí se realizarían validaciones más robustas (ej. luhn algorithm, fecha futura)
        # Por simplicidad, solo una validación básica de longitud.
        if not (data['expiry_month'].isdigit() and len(data['expiry_month']) == 2):
            raise serializers.ValidationError("El mes de expiración debe ser un número de dos dígitos.")
        if not (data['expiry_year'].isdigit() and len(data['expiry_year']) == 4):
            raise serializers.ValidationError("El año de expiración debe ser un número de cuatro dígitos.")
        return data

class PaymentInitiationSerializer(serializers.Serializer):
    """
    Serializador para iniciar un nuevo pago.
    """
    user_id = serializers.CharField(max_length=255, help_text="ID del usuario que inicia el pago")
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01, help_text="Monto a pagar")
    currency = serializers.CharField(max_length=3, default='USD', help_text="Moneda de la transacción (ej. 'USD', 'EUR')")
    card_details = CardDetailsSerializer(help_text="Detalles de la tarjeta de crédito para el pago")
    save_method = serializers.BooleanField(default=False, help_text="Indica si se debe guardar el método de pago para futuras compras")

class PaymentConfirmationSerializer(serializers.Serializer):
    """
    Serializador para la confirmación de pago (ej. desde un webhook de pasarela).
    """
    transaction_id = serializers.UUIDField(help_text="ID interno de la transacción de pago")
    gateway_reference_id = serializers.CharField(max_length=255, help_text="ID de referencia de la pasarela de pago")
    status = serializers.CharField(max_length=10, help_text="Estado final de la transacción (ej. 'COMPLETED', 'FAILED')")
    # Podría incluir un campo JSON para la respuesta completa de la pasarela si fuera necesario.
    gateway_response = serializers.JSONField(required=False, help_text="Respuesta completa de la pasarela de pago")


class SavedPaymentMethodSerializer(serializers.ModelSerializer):
    """
    Serializador para la representación de métodos de pago guardados.
    """
    class Meta:
        model = SavedPaymentMethod
        fields = ['id', 'card_brand', 'last_four_digits', 'expiration_date', 'is_default', 'created_at']
        read_only_fields = ['id', 'card_brand', 'last_four_digits', 'expiration_date', 'created_at']
