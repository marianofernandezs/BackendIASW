"""
Definiciones de URL para la aplicación support_chat.
Mapea las rutas de la API a las vistas correspondientes.
"""

from django.urls import path
from src.support_chat.views import ChatSessionAPIView, ChatMessageAPIView, chat_session_list,create_chat_session,chat_room

app_name = 'support_chat'

urlpatterns = [
    # Ruta para crear una nueva sesión de chat.
    path('api/sessions/', ChatSessionAPIView.as_view(), name='chat-session-list-create'),
    # Rutas para obtener una sesión específica y enviar/recibir mensajes.
    path('api/sessions/<int:session_id>/', ChatSessionAPIView.as_view(), name='chat-session-detail'),
    path('api/sessions/<int:session_id>/messages/', ChatMessageAPIView.as_view(), name='chat-message-list-create'),

      path("sessions/", chat_session_list, name="chat_session_list"),
      path("sessions/new/", create_chat_session, name="create_session"),
      path("sessions/<int:session_id>/", chat_room, name="chat_room"),
]
