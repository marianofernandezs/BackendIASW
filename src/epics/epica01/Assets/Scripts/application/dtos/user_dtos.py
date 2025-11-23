from pydantic import BaseModel, EmailStr, Field

class UserRegistrationRequest(BaseModel):
    """
    DTO para la solicitud de registro de usuario.
    Contiene los datos de entrada para el caso de uso de registro.
    """
    email: EmailStr = Field(..., description="Email del usuario para el registro.")
    password: str = Field(..., min_length=8, description="Contraseña del usuario.") # La validación completa se hará en Domain/Password.

class UserRegistrationResponse(BaseModel):
    """
    DTO para la respuesta del registro de usuario.
    Contiene el resultado de la operación de registro.
    """
    user_id: str = Field(None, description="ID del usuario registrado, si la operación fue exitosa.")
    email: EmailStr = Field(..., description="Email del usuario intentado registrar.")
    message: str = Field(..., description="Mensaje descriptivo del resultado de la operación.")
    success: bool = Field(..., description="Indica si la operación de registro fue exitosa.")
