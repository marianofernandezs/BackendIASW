"""
Serializadores para los modelos de la aplicación support_chat.
Convierten objetos de modelo a formatos JSON y viceversa para las APIs.
"""

from rest_framework import serializers
from support_chat.models import ChatSession, ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo ChatMessage.
    Incluye todos los campos de lectura y escritura.
    """
    class Meta:
        model = ChatMessage
        fields = ['id', 'session', 'sender', 'content', 'timestamp']
        read_only_fields = ['id', 'sender', 'timestamp'] # El remitente y la marca de tiempo se gestionan por el sistema.


class ChatSessionSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo ChatSession.
    Incluye todos los campos y una representación anidada de los mensajes.
    """
    # Campo para mostrar los mensajes asociados a la sesión (lectura solamente).
    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatSession
        fields = ['id', 'created_at', 'updated_at', 'status', 'messages']
        read_only_fields = ['id', 'created_at', 'updated_at', 'status'] # Estos campos son gestionados por el sistema.
