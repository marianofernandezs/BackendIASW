import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto

class Entity:
    """Clase base para todas las entidades con un ID único."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

@dataclass
class User(Entity):
    """Representa a un usuario final del sistema."""
    name: str

@dataclass
class SupportAgent(Entity):
    """Representa a un agente de soporte humano."""
    name: str
    is_online: bool = True

class MessageSender(Enum):
    """Enumeración para el tipo de emisor de un mensaje."""
    USER = auto()
    AGENT = auto()
    BOT = auto()
    SYSTEM = auto()

@dataclass
class Message(Entity):
    """Representa un mensaje individual dentro de una sesión de chat."""
    sender: MessageSender
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    session_id: str = "" # ID de la sesión a la que pertenece el mensaje

class ChatSessionStatus(Enum):
    """Estado actual de una sesión de chat."""
    OPEN = auto()
    IN_PROGRESS = auto()
    CLOSED = auto()
    PENDING_AGENT = auto()

@dataclass
class ChatSession(Entity):
    """Representa una sesión de chat entre un usuario y el soporte."""
    user_id: str
    messages: list[Message] = field(default_factory=list)
    status: ChatSessionStatus = ChatSessionStatus.OPEN
    agent_id: str | None = None
    start_time: datetime = field(default_factory=datetime.now)
    end_time: datetime | None = None

    def add_message(self, message: Message):
        """Añade un mensaje a la sesión."""
        self.messages.append(message)

# --- Entidades Placeholder para Inventario y Crafting ---
@dataclass
class Item(Entity):
    """Placeholder: Representa un item en el inventario."""
    name: str
    description: str
    quantity: int = 1

@dataclass
class CraftingRecipe(Entity):
    """Placeholder: Define una receta de crafteo."""
    name: str
    output_item_id: str
    output_quantity: int
    required_items: dict[str, int] # {item_id: quantity}
    difficulty: int = 1
