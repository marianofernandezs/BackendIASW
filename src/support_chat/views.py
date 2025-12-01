"""
Vistas de la API para la aplicación support_chat.
Manejan las solicitudes HTTP para sesiones de chat y mensajes.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction # Para asegurar la atomicidad en operaciones.

from support_chat.models import ChatSession
from support_chat.serializers import ChatSessionSerializer, ChatMessageSerializer
from support_chat.services import (
    AgentAvailabilityService, BotService, AgentService,
    MessagePersistenceService, ChatSessionService, ChatOrchestratorService
)


class ChatSessionAPIView(APIView):
    """
    Vista para crear nuevas sesiones de chat y obtener una sesión existente.
    """
    # Inyección de dependencias para los servicios
    _chat_session_service = ChatSessionService()
    _message_persistence_service = MessagePersistenceService()

    def post(self, request):
        """
        Crea una nueva sesión de chat.
        """
        with transaction.atomic():
            session = self._chat_session_service.create_session()
            # Opcional: añadir un mensaje de bienvenida del bot al inicio de la sesión.
            # self._message_persistence_service.save_message(
            #    session, 'bot', "¡Hola! ¿En qué podemos ayudarte hoy?"
            # )
            serializer = ChatSessionSerializer(session)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, session_id):
        """
        Obtiene los detalles de una sesión de chat específica.
        """
        session = get_object_or_404(ChatSession, id=session_id)
        # Asegurarse de que los mensajes se carguen para el serializador.
        session_with_messages = ChatSession.objects.prefetch_related('messages').get(id=session_id)
        serializer = ChatSessionSerializer(session_with_messages)
        return Response(serializer.data)


class ChatMessageAPIView(APIView):
    """
    Vista para enviar mensajes a una sesión de chat y obtener todos los mensajes de una sesión.
    """
    # Inyección de dependencias para el orquestador de chat
    _chat_orchestrator_service = ChatOrchestratorService(
        agent_availability_service=AgentAvailabilityService(),
        bot_service=BotService(),
        agent_service=AgentService(),
        message_persistence_service=MessagePersistenceService(),
        chat_session_service=ChatSessionService()
    )
    _message_persistence_service = MessagePersistenceService() # También se necesita para listar mensajes
    _chat_session_service = ChatSessionService() # Para obtener la sesión antes de listar mensajes

    def post(self, request, session_id):
        """
        Envía un nuevo mensaje del cliente a la sesión y genera una respuesta.
        """
        try:
            session = self._chat_session_service.get_session(session_id)
        except ChatSession.DoesNotExist:
            return Response({"detail": "Sesión de chat no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ChatMessageSerializer(data=request.data)
        if serializer.is_valid():
            client_message_content = serializer.validated_data['content']

            with transaction.atomic():
                # El orquestador maneja la persistencia del mensaje del cliente y la respuesta.
                response_message = self._chat_orchestrator_service.handle_incoming_message(
                    session_id, client_message_content
                )
                response_serializer = ChatMessageSerializer(response_message)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, session_id):
        """
        Obtiene todos los mensajes para una sesión de chat específica.
        """
        try:
            session = self._chat_session_service.get_session(session_id)
        except ChatSession.DoesNotExist:
            return Response({"detail": "Sesión de chat no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        messages = self._message_persistence_service.get_messages_for_session(session)
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)
