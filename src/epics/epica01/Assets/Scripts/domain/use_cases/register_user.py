from abc import ABC, abstractmethod
from typing import NamedTuple

# DTOs de Request/Response se definen en la capa de aplicación,
# pero el caso de uso los referencia por contrato.
# Para evitar dependencia circular, podemos usar NamedTuple o clases
# sencillas aquí, o simplemente definir las interfaces y que la capa
# de aplicación las concrete. Para simplificar el ejemplo,
# se asumen los DTOs de la capa de aplicación.

class UserRegistrationRequestDTO(NamedTuple):
    email: str
    password: str

class UserRegistrationResponseDTO(NamedTuple):
    user_id: str
    email: str
    message: str
    success: bool

class IRegisterUserUseCase(ABC):
    """
    Interfaz abstracta para el caso de uso de registro de usuario.
    Define el contrato para la ejecución del registro.
    """

    @abstractmethod
    def execute(self, request: UserRegistrationRequestDTO) -> UserRegistrationResponseDTO:
        """
        Ejecuta el proceso de registro de un nuevo usuario.
        :param request: Objeto con los datos de registro (email, contraseña).
        :return: Objeto con el resultado del registro (ID de usuario, mensaje, éxito).
        """
        pass
