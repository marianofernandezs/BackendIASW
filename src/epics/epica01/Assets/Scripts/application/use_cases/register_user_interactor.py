from Assets.Scripts.domain.entities.user import User
from Assets.Scripts.domain.repositories.user_repository import IUserRepository
from Assets.Scripts.domain.services.password_service import IPasswordService
from Assets.Scripts.domain.use_cases.register_user import IRegisterUserUseCase
from Assets.Scripts.domain.value_objects.email import Email
from Assets.Scripts.domain.value_objects.password import Password
from Assets.Scripts.application.dtos.user_dtos import UserRegistrationRequest, UserRegistrationResponse

class RegisterUserInteractor(IRegisterUserUseCase):
    """
    Implementación del caso de uso para registrar un nuevo usuario.
    Orquesta la lógica de negocio para la creación de cuentas.
    """

    def __init__(self, user_repository: IUserRepository, password_service: IPasswordService):
        """
        Constructor del interactor.
        Inyecta las dependencias necesarias: repositorio de usuarios y servicio de contraseñas.
        """
        self._user_repository = user_repository
        self._password_service = password_service

    def execute(self, request: UserRegistrationRequest) -> UserRegistrationResponse:
        """
        Ejecuta el proceso de registro de usuario.
        """
        try:
            # 1. Validar email (formato) y contraseña (política) con Value Objects
            email_vo = Email(request.email)
            password_vo = Password(request.password) # Esto valida la política de contraseña

            # 2. Verificar si el email ya está registrado
            if self._user_repository.email_exists(email_vo):
                return UserRegistrationResponse(
                    user_id=None,
                    email=request.email,
                    message="El email ya está en uso.",
                    success=False
                )

            # 3. Hashear la contraseña
            hashed_password = self._password_service.hash_password(password_vo.value)

            # 4. Crear la entidad User
            new_user = User(email=email_vo, password_hash=hashed_password)

            # 5. Persistir el usuario
            saved_user = self._user_repository.save(new_user)

            # 6. Retornar una respuesta exitosa
            return UserRegistrationResponse(
                user_id=saved_user.id,
                email=saved_user.email.value,
                message="Cuenta creada exitosamente.",
                success=True
            )

        except ValueError as e:
            # Captura errores de validación de Value Objects
            return UserRegistrationResponse(
                user_id=None,
                email=request.email,
                message=f"Error de validación: {e}",
                success=False
            )
        except Exception as e:
            # Captura otros errores inesperados
            return UserRegistrationResponse(
                user_id=None,
                email=request.email,
                message=f"Error inesperado al registrar usuario: {e}",
                success=False
            )
