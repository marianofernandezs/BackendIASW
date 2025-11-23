import re
from pydantic import BaseModel, Field, ValidationError

class Email(BaseModel):
    """
    Objeto de valor para Email.
    Encapsula la validación del formato del email.
    """
    value: str = Field(..., description="Dirección de correo electrónico.")

    class Config:
        frozen = True  # Los objetos de valor son inmutables.

    @classmethod
    def validate_email_format(cls, email: str) -> bool:
        """Valida el formato de un email."""
        # Regex básico para email, puede ser más complejo si se requiere.
        email_regex = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
        return bool(email_regex.match(email))

    def __init__(self, value: str):
        super().__init__(value=value)
        if not self.validate_email_format(value):
            raise ValueError("Formato de email inválido.")

    def __str__(self):
        """Representación en cadena del email."""
        return self.value

    def __hash__(self):
        """Permite usar Email en conjuntos y como claves de diccionario."""
        return hash(self.value)
