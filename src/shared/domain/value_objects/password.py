import re
from pydantic import BaseModel, Field

class Password(BaseModel):
    """
    Objeto de valor para Contraseña.
    Encapsula la validación de la política de seguridad de la contraseña.
    NO ALMACENA EL HASH, solo el texto plano para validación inicial.
    """
    value: str = Field(..., description="Contraseña en texto plano.")

    class Config:
        frozen = True # Los objetos de valor son inmutables.

    @classmethod
    def validate_password_policy(cls, password: str) -> bool:
        """
        Valida que la contraseña cumpla la política:
        - Mínimo 8 caracteres.
        - Al menos 1 mayúscula.
        - Al menos 1 dígito.
        """
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):
            return False  # No mayúscula
        if not re.search(r"\d", password):
            return False  # No dígito
        return True

    def __init__(self, value: str):
        super().__init__(value=value)
        if not self.validate_password_policy(value):
            raise ValueError(
                "La contraseña debe tener al menos 8 caracteres, "
                "incluir una mayúscula y un dígito."
            )

    def __str__(self):
        """No exponer la contraseña en texto plano, usar una representación segura."""
        return "********" # Nunca retornar la contraseña real.
