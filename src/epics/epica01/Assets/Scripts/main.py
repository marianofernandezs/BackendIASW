from Assets.Scripts.infrastructure.config import AppConfig
from Assets.Scripts.presentation.controllers.registration_controller import RegistrationController

def run_registration_scenario(controller: RegistrationController, email: str, password: str, scenario_name: str):
    """Función auxiliar para ejecutar y mostrar resultados de un escenario de registro."""
    print(f"\n--- Escenario: {scenario_name} ---")
    response = controller.register_user(email, password)
    print(f"Email: {response.email}")
    print(f"Mensaje: {response.message}")
    print(f"Éxito: {response.success}")
    if response.success:
        print(f"ID de Usuario: {response.user_id}")

if __name__ == "__main__":
    # Inicializar configuración de la aplicación
    app_config = AppConfig()

    # Obtener el controlador de registro a través de la configuración
    registration_controller = RegistrationController(
        register_user_use_case=app_config.get_register_user_use_case()
    )

    # Escenarios de prueba basados en US-01

    # Escenario 1: Registro exitoso con credenciales válidas
    run_registration_scenario(
        registration_controller,
        "ana@example.com",
        "Clave2025",
        "Registro exitoso con credenciales válidas"
    )
    # Escenario 1.1: Otro registro exitoso
    run_registration_scenario(
        registration_controller,
        "pedro@example.org",
        "Pedro99@example.org",
        "Otro registro exitoso"
    )

    # Escenario 2: Email ya registrado
    run_registration_scenario(
        registration_controller,
        "ana@example.com",
        "NuevaClave2026",
        "Email ya registrado"
    )

    # Escenario 3: Contraseña no cumple política (muy corta)
    run_registration_scenario(
        registration_controller,
        "nuevo@example.com",
        "abc",
        "Contraseña no cumple política (muy corta)"
    )

    # Escenario 3.1: Contraseña no cumple política (sin mayúscula)
    run_registration_scenario(
        registration_controller,
        "otro@example.com",
        "clave123",
        "Contraseña no cumple política (sin mayúscula)"
    )

    # Escenario 3.2: Contraseña no cumple política (sin dígito)
    run_registration_scenario(
        registration_controller,
        "mas@example.com",
        "ClaveSegura",
        "Contraseña no cumple política (sin dígito)"
    )

    # Escenario 4: Formato de email inválido
    run_registration_scenario(
        registration_controller,
        "email-invalido",
        "ClaveValida123",
        "Formato de email inválido"
    )
