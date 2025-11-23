import json
import os
from typing import TypeVar, Type, Optional, Dict, List
from abc import ABC
from datetime import datetime

from domain.entities import Entity, Message, ChatSession, User, Item, CraftingRecipe
from application.interfaces.repositories import (
    IRepository, IMessageRepository, IUserRepository, IInventoryRepository, ICraftingRepository
)

T = TypeVar('T', bound=Entity)

class JsonRepository(IRepository[T], ABC):
    """
    Clase base abstracta para repositorios que persisten entidades en archivos JSON.
    Simula una base de datos simple en memoria cargada desde/guardada en un archivo.
    """
    def __init__(self, entity_type: Type[T], filepath: str):
        self._entity_type = entity_type
        self._filepath = filepath
        self._data: Dict[str, T] = {}
        self._load_data()

    def _serialize_entity(self, entity: T) -> Dict[str, Any]:
        """Convierte una entidad a un diccionario serializable."""
        # Se usa una función personalizada para manejar dataclasses y enums
        data = entity.__dict__.copy()
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
            elif isinstance(value, list) and all(isinstance(item, Entity) for item in value):
                data[key] = [self._serialize_entity(item) for item in value]
            elif isinstance(value, list) and all(isinstance(item, (int, str, float, bool)) for item in value):
                pass # Primitivos en lista se mantienen
            elif hasattr(value, 'value'): # Para Enums
                data[key] = value.value
        return data

    def _deserialize_data(self, data: Dict[str, Any]) -> T:
        """Convierte un diccionario a una entidad."""
        # Necesitamos recrear el objeto con sus tipos originales
        # Esto es más complejo para anidados, pero para este ejemplo,
        # nos centraremos en Message y ChatSession.
        # Un enfoque robusto usaría un framework de serialización como Pydantic.
        if self._entity_type == ChatSession:
            messages_data = data.pop('messages', [])
            messages = [Message(session_id=data['id'], **self._deserialize_message_dict(msg_data)) for msg_data in messages_data]
            data['messages'] = messages
            
        # Convertir campos de fecha si existen
        for key, value in data.items():
            if isinstance(value, str):
                try:
                    # Intenta parsear como ISO 8601, si falla, no es una fecha
                    data[key] = datetime.fromisoformat(value)
                except (ValueError, TypeError):
                    pass
            # Deserializar enums si se guardaron por valor
            if key == 'sender' and 'MessageSender' in str(self._entity_type.__annotations__.get(key)):
                 from domain.entities import MessageSender
                 data[key] = MessageSender(value)
            elif key == 'status' and 'ChatSessionStatus' in str(self._entity_type.__annotations__.get(key)):
                from domain.entities import ChatSessionStatus
                data[key] = ChatSessionStatus(value)
            
        return self._entity_type(**data)

    def _deserialize_message_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Helper para deserializar un diccionario de mensaje."""
        from domain.entities import MessageSender
        deserialized = data.copy()
        if 'timestamp' in deserialized and isinstance(deserialized['timestamp'], str):
            deserialized['timestamp'] = datetime.fromisoformat(deserialized['timestamp'])
        if 'sender' in deserialized and isinstance(deserialized['sender'], int):
            deserialized['sender'] = MessageSender(deserialized['sender'])
        return deserialized

    def _load_data(self):
        """Carga datos desde el archivo JSON."""
        if os.path.exists(self._filepath):
            with open(self._filepath, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
                self._data = {item['id']: self._deserialize_data(item) for item in raw_data}
        else:
            self._data = {}

    def _save_data(self):
        """Guarda los datos en el archivo JSON."""
        os.makedirs(os.path.dirname(self._filepath), exist_ok=True)
        serializable_data = [self._serialize_entity(entity) for entity in self._data.values()]
        with open(self._filepath, 'w', encoding='utf-8') as f:
            json.dump(serializable_data, f, indent=4, ensure_ascii=False)

    def get_by_id(self, entity_id: str) -> Optional[T]:
        """Obtiene una entidad por su ID."""
        return self._data.get(entity_id)

    def save(self, entity: T):
        """Guarda o actualiza una entidad."""
        self._data[entity.id] = entity
        self._save_data() # Persiste inmediatamente para este ejemplo
        print(f"DEBUG: Saved {self._entity_type.__name__} with ID: {entity.id}")


    def delete(self, entity_id: str):
        """Elimina una entidad por su ID."""
        if entity_id in self._data:
            del self._data[entity_id]
            self._save_data()

    def get_all(self) -> list[T]:
        """Obtiene todas las entidades."""
        return list(self._data.values())

class JsonMessageRepository(JsonRepository[ChatSession], IMessageRepository):
    """Implementación de IMessageRepository usando archivos JSON."""
    def __init__(self, filepath: str = 'data/chat_sessions.json'):
        super().__init__(ChatSession, filepath)

    def get_session_by_user_id(self, user_id: str) -> Optional[ChatSession]:
        """Obtiene una sesión de chat activa para un usuario."""
        for session in self._data.values():
            if session.user_id == user_id and session.status != ChatSessionStatus.CLOSED:
                return session
        return None

class JsonUserRepository(JsonRepository[User], IUserRepository):
    """Implementación de IUserRepository usando archivos JSON."""
    def __init__(self, filepath: str = 'data/users.json'):
        super().__init__(User, filepath)

class JsonInventoryRepository(JsonRepository[Item], IInventoryRepository):
    """Placeholder: Implementación de IInventoryRepository usando archivos JSON."""
    def __init__(self, filepath: str = 'data/inventory.json'):
        super().__init__(Item, filepath)

class JsonCraftingRepository(JsonRepository[CraftingRecipe], ICraftingRepository):
    """Placeholder: Implementación de ICraftingRepository usando archivos JSON."""
    def __init__(self, filepath: str = 'data/crafting_recipes.json'):
        super().__init__(CraftingRecipe, filepath)
