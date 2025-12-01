"""
Definiciones de URL para la aplicación support_chat.
Mapea las rutas de la API a las vistas correspondientes.
"""

from django.urls import path
from src.support_chat.views import ChatSessionAPIView, ChatMessageAPIView

app_name = 'support_chat'

urlpatterns = [
    # Ruta para crear una nueva sesión de chat.
    path('sessions/', ChatSessionAPIView.as_view(), name='chat-session-list-create'),
    # Rutas para obtener una sesión específica y enviar/recibir mensajes.
    path('sessions/<int:session_id>/', ChatSessionAPIView.as_view(), name='chat-session-detail'),
    path('sessions/<int:session_id>/messages/', ChatMessageAPIView.as_view(), name='chat-message-list-create'),
]
