"""
Modelos de base de datos para la aplicación support_chat.
Define la estructura de las sesiones de chat y los mensajes.
"""

from django.db import models


class ChatSession(models.Model):
    """
    Representa una sesión de chat individual entre un cliente y el soporte.
    """
    # Fecha y hora de creación de la sesión.
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    # Fecha y hora de la última actualización de la sesión.
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    # Estado de la sesión (ej. 'abierta', 'cerrada', 'esperando agente').
    # Podría expandirse con más estados si es necesario.
    status = models.CharField(
        max_length=50,
        default='open',
        verbose_name="Estado de la Sesión",
        help_text="Estado actual de la sesión de chat (ej. 'open', 'closed')."
    )

    class Meta:
        verbose_name = "Sesión de Chat"
        verbose_name_plural = "Sesiones de Chat"
        ordering = ['-created_at'] # Ordenar sesiones por las más recientes primero.

    def __str__(self):
        return f"Sesión #{self.id} - {self.status} (Creada: {self.created_at.strftime('%Y-%m-%d %H:%M')})"


class ChatMessage(models.Model):
    """
    Representa un mensaje individual dentro de una sesión de chat.
    """
    # Clave foránea a la sesión de chat a la que pertenece este mensaje.
    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE, # Si se elimina la sesión, se eliminan sus mensajes.
        related_name='messages', # Nombre para acceder a los mensajes desde una sesión.
        verbose_name="Sesión de Chat"
    )
    # Identificador del remitente del mensaje (ej. 'client', 'agent', 'bot').
    sender = models.CharField(
        max_length=50,
        verbose_name="Remitente",
        help_text="Quién envió el mensaje (ej. 'client', 'agent', 'bot')."
    )
    # Contenido textual del mensaje.
    content = models.TextField(verbose_name="Contenido del Mensaje")
    # Marca de tiempo cuando el mensaje fue enviado.
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Marca de Tiempo")

    class Meta:
        verbose_name = "Mensaje de Chat"
        verbose_name_plural = "Mensajes de Chat"
        ordering = ['timestamp'] # Ordenar mensajes cronológicamente.

    def __str__(self):
        return f"Sesión {self.session.id} - {self.sender}: {self.content[:50]}"
