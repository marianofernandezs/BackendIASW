from rest_framework import serializers
from .models import DeliveryPersonProfile

class DeliveryContactSerializer(serializers.ModelSerializer):
    """
    Serializa los datos de contacto del repartidor del pedido (HU10).
    Incluye nombre desde el usuario asociado.
    """
    name = serializers.SerializerMethodField()

    class Meta:
        model = DeliveryPersonProfile
        fields = ['name', 'email', 'phone']

    def get_name(self, obj):
        user = obj.user
        # Si existe first_name + last_name, úsalo | de lo contrario username
        full = f"{user.first_name} {user.last_name}".strip()
        return full if full else user.username
