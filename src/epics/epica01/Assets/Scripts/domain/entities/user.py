import uuid
from pydantic import BaseModel, Field
from datetime import datetime

from Assets.Scripts.domain.value_objects.email import Email

class User(BaseModel):
    """
    Entidad de dominio para un Usuario.
    Representa una cuenta de usuario con sus atributos principales.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="ID único del usuario.")
    email: Email = Field(..., description="Email del usuario (objeto de valor).")
    password_hash: str = Field(..., min_length=1, description="Hash de la contraseña del usuario.")
    is_active: bool = Field(default=True, description="Indica si la cuenta está activa.")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Fecha de creación de la cuenta.")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Fecha de última actualización de la cuenta.")

    def update_email(self, new_email: Email):
        """Actualiza el email del usuario."""
        if self.email != new_email:
            self.email = new_email
            self.updated_at = datetime.utcnow()

    def deactivate(self):
        """Desactiva la cuenta del usuario."""
        if self.is_active:
            self.is_active = False
            self.updated_at = datetime.utcnow()

    def activate(self):
        """Activa la cuenta del usuario."""
        if not self.is_active:
            self.is_active = True
            self.updated_at = datetime.utcnow()
