from typing import Any, Type

from application.interfaces.repositories import (
    IMessageRepository, IUserRepository, IInventoryRepository, ICraftingRepository
)

class PersistenceManager:
    """
    Gestor central de persistencia que coordina diferentes repositorios.
    Asegura que todos los datos se persistan o carguen de manera consistente.
    """
    def __init__(self,
                 message_repo: IMessageRepository,
                 user_repo: IUserRepository,
                 inventory_repo: IInventoryRepository, # Placeholder
                 crafting_repo: ICraftingRepository):  # Placeholder
        self.message_repo = message_repo
        self.user_repo = user_repo
        self.inventory_repo = inventory_repo
        self.crafting_repo = crafting_repo

    def save_all(self):
        """Método para guardar todos los cambios pendientes en todos los repositorios.
           (En una implementación más compleja, esto podría ser transaccional).
        """
        # Para el ejemplo con JsonRepository, 'save' se hace por entidad,
        # pero aquí podría haber una lógica de "commit" general.
        print("DEBUG: PersistenceManager.save_all called (no-op for JSON repo).")

    def load_all(self):
        """Método para cargar todos los datos iniciales. (Placeholder)."""
        print("DEBUG: PersistenceManager.load_all called (no-op for JSON repo).")

    def get_repository(self, repo_type: Type[Any]) -> Any:
        """Permite obtener un repositorio por su tipo (para inyección manual o Testing)."""
        if repo_type == IMessageRepository:
            return self.message_repo
        if repo_type == IUserRepository:
            return self.user_repo
        if repo_type == IInventoryRepository:
            return self.inventory_repo
        if repo_type == ICraftingRepository:
            return self.crafting_repo
        raise ValueError(f"Repositorio de tipo {repo_type} no registrado.")
