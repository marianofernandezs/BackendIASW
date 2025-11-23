from Assets.Scripts.application.dtos.user_dtos import UserRegistrationRequest, UserRegistrationResponse
from Assets.Scripts.domain.use_cases.register_user import IRegisterUserUseCase
from pydantic import ValidationError

class RegistrationController:
    """
    Controlador de registro de usuario.
    Recibe las peticiones de la interfaz (simulada), las convierte a DTOs
    y llama al caso de uso de aplicación.
    """

    def __init__(self, register_user_use_case: IRegisterUserUseCase):
        """
        Constructor del controlador.
        Inyecta la interfaz del caso de uso de registro.
        """
        self._register_user_use_case = register_user_use_case

    def register_user(self, email: str, password: str) -> UserRegistrationResponse:
        """
        Procesa una petición de registro de usuario.
        :param email: Email proporcionado por el usuario.
        :param password: Contraseña proporcionada por el usuario.
        :return: DTO con el resultado del registro.
        """
        try:
            # Convertir datos crudos a DTO de Request
            request_dto = UserRegistrationRequest(email=email, password=password)

            # Invocar el caso de uso de aplicación
            response_dto = self._register_user_use_case.execute(request_dto)
            return response_dto
        except ValidationError as e:
            # Capturar errores de validación de Pydantic para el DTO de Request
            return UserRegistrationResponse(
                user_id=None,
                email=email,
                message=f"Error en los datos de entrada: {e.errors()}",
                success=False
            )
        except Exception as e:
            # Capturar cualquier otro error inesperado en la capa de presentación
            return UserRegistrationResponse(
                user_id=None,
                email=email,
                message=f"Error inesperado en el controlador: {e}",
                success=False
            )
