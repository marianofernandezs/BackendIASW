from rest_framework import serializers
from payment_methods.models import PaymentMethod

class PaymentMethodSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo PaymentMethod.
    Expone los campos necesarios para la API sin revelar datos sensibles (como el token
    del gateway, que debe permanecer interno).
    """
    class Meta:
        model = PaymentMethod
        fields = [
            'id', 'brand', 'last_four_digits', 'expiry_month', 'expiry_year',
            'is_default', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class PaymentMethodSaveSerializer(serializers.Serializer):
    """
    Serializador para la entrada de datos al guardar un nuevo método de pago.
    Requiere el token y metadatos del gateway, más el consentimiento del usuario.
    """
    token = serializers.CharField(max_length=255, help_text="Token de pago proporcionado por la pasarela.")
    brand = serializers.CharField(max_length=50, help_text="Marca de la tarjeta (ej. Visa, Mastercard).")
    last_four_digits = serializers.CharField(max_length=4, help_text="Últimos cuatro dígitos de la tarjeta.")
    expiry_month = serializers.IntegerField(min_value=1, max_value=12, help_text="Mes de expiración (1-12).")
    expiry_year = serializers.IntegerField(min_value=2000, max_value=2099, help_text="Año de expiración.") # Ajustar rango según necesidad
    save_card = serializers.BooleanField(default=False, help_text="Indica si el usuario desea guardar la tarjeta.")

    def validate(self, data):
        """
        Validación adicional, por ejemplo, para la lógica de fechas de expiración.
        """
        # Aquí se podría añadir lógica para verificar que la tarjeta no está expirada.
        # Por simplicidad, se omite para esta iteración.
        return data
