import sys
import os

# Añadir el directorio 'Assets/Scripts' al path para las importaciones relativas
# Esto es un workaround para el entorno de ejecución, en un proyecto real se configuraría Python Path.
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Importaciones de las capas de la arquitectura
from Application.Interfaces.product_repository import IProductRepository
from Application.Interfaces.category_repository import ICategoryRepository
from Application.Interfaces.inventory_repository import IInventoryRepository
from Application.Interfaces.recipe_repository import IRecipeRepository
from Application.Interfaces.persistence_service import IPersistenceService

from Infrastructure.Repositories.in_memory_product_repository import InMemoryProductRepository
from Infrastructure.Repositories.in_memory_category_repository import InMemoryCategoryRepository
from Infrastructure.Repositories.in_memory_inventory_repository import InMemoryInventoryRepository
from Infrastructure.Repositories.in_memory_recipe_repository import InMemoryRecipeRepository
from Infrastructure.Persistence.json_file_persistence_service import JsonFilePersistenceService
from Infrastructure.Config.initial_data_config import InitialDataConfig

from Application.UseCases.get_product_catalog_use_case import GetProductCatalogUseCase
from Application.UseCases.get_product_details_use_case import GetProductDetailsUseCase
from Application.UseCases.craft_item_use_case import CraftItemUseCase
from Application.UseCases.update_inventory_use_case import UpdateInventoryUseCase
from Application.UseCases.load_initial_data_use_case import LoadInitialDataUseCase
from Application.UseCases.save_data_use_case import SaveDataUseCase

from Application.DTOs.catalog_dtos import GetCatalogRequest
from Application.DTOs.crafting_dtos import CraftItemRequest
from Domain.Exceptions.custom_exceptions import ProductNotFoundException, RecipeNotFoundException, InsufficientStockException, DomainException

class CLIApp:
    """
    Aplicación de Línea de Comandos (CLI) para interactuar con el sistema.
    Realiza la inyección de dependencias y maneja la interfaz de usuario.
    """
    PERSISTENCE_FILE = "game_data.json"

    def __init__(self):
        # Configuración e Inyección de Dependencias
        self._initial_data_config = InitialDataConfig()

        self._product_repo: IProductRepository = InMemoryProductRepository()
        self._category_repo: ICategoryRepository = InMemoryCategoryRepository()
        self._inventory_repo: IInventoryRepository = InMemoryInventoryRepository()
        self._recipe_repo: IRecipeRepository = InMemoryRecipeRepository()
        self._persistence_service: IPersistenceService = JsonFilePersistenceService()

        # Casos de Uso
        self._load_initial_data_use_case = LoadInitialDataUseCase(
            product_repo=self._product_repo,
            category_repo=self._category_repo,
            inventory_repo=self._inventory_repo,
            recipe_repo=self._recipe_repo,
            persistence_service=self._persistence_service,
            initial_data_config=self._initial_data_config,
            persistence_file_path=self.PERSISTENCE_FILE
        )
        self._save_data_use_case = SaveDataUseCase(
            product_repo=self._product_repo,
            category_repo=self._category_repo,
            inventory_repo=self._inventory_repo,
            recipe_repo=self._recipe_repo,
            persistence_service=self._persistence_service,
            persistence_file_path=self.PERSISTENCE_FILE
        )
        self._get_product_catalog_use_case = GetProductCatalogUseCase(
            product_repo=self._product_repo,
            category_repo=self._category_repo
        )
        self._get_product_details_use_case = GetProductDetailsUseCase(
            product_repo=self._product_repo,
            category_repo=self._category_repo
        )
        self._craft_item_use_case = CraftItemUseCase(
            recipe_repo=self._recipe_repo,
            inventory_repo=self._inventory_repo,
            product_repo=self._product_repo
        )
        self._update_inventory_use_case = UpdateInventoryUseCase(
            inventory_repo=self._inventory_repo,
            product_repo=self._product_repo
        )

        self._load_initial_data_use_case.execute() # Cargar datos al inicio

    def _display_menu(self):
        """Muestra el menú principal de la aplicación."""
        print("\n--- Menú Principal ---")
        print("1. Ver Catálogo de Productos")
        print("2. Ver Detalles de Producto")
        print("3. Craftear un Ítem")
        print("4. Mostrar Inventario")
        print("5. Añadir Stock al Inventario")
        print("6. Guardar Datos")
        print("0. Salir")
        print("--------------------")

    def run(self):
        """Inicia el bucle principal de la aplicación CLI."""
        while True:
            self._display_menu()
            choice = input("Seleccione una opción: ")

            if choice == '1':
                self._view_catalog()
            elif choice == '2':
                self._view_product_details()
            elif choice == '3':
                self._craft_item()
            elif choice == '4':
                self._show_inventory()
            elif choice == '5':
                self._add_stock_to_inventory()
            elif choice == '6':
                self._save_data_use_case.execute()
            elif choice == '0':
                print("Saliendo del sistema. ¡Hasta pronto!")
                break
            else:
                print("Opción no válida. Por favor, intente de nuevo.")

    def _view_catalog(self):
        """Muestra el catálogo de productos con paginación y filtros."""
        print("\n--- Catálogo de Productos ---")
        page = 1
        page_size = 12
        search_term: Optional[str] = None
        category_id: Optional[str] = None

        while True:
            request = GetCatalogRequest(
                page=page,
                page_size=page_size,
                search_term=search_term,
                category_id=category_id
            )
            response = self._get_product_catalog_use_case.execute(request)

            if not response.items:
                print("No hay productos disponibles con los criterios actuales.")
                if search_term or category_id:
                    print(f"Búsqueda: '{search_term or 'N/A'}', Categoría: '{category_id or 'N/A'}'")
            else:
                print(f"Página {response.paging_info.current_page} de {response.paging_info.total_pages} (Total: {response.paging_info.total_items} productos)")
                print("-" * 50)
                for item in response.items:
                    availability = "Disponible" if item.is_available else "Sin Stock"
                    print(f"ID: {item.id:<8} | Nombre: {item.name:<25} | Precio: ${item.price:>6.2f} | Categoría: {item.category_name:<15} | {availability}")
                print("-" * 50)

            print("\nOpciones de Navegación:")
            print("  <Enter> o 's': Siguiente página")
            print("  'a': Página anterior")
            print("  'b': Volver al menú principal")
            print("  'f': Aplicar filtros (búsqueda, categoría)")
            print("  'r': Reiniciar filtros")
            action = input("Acción: ").lower()

            if action == '' or action == 's':
                if page < response.paging_info.total_pages:
                    page += 1
                else:
                    print("Ya estás en la última página.")
            elif action == 'a':
                if page > 1:
                    page -= 1
                else:
                    print("Ya estás en la primera página.")
            elif action == 'f':
                search_term_input = input("Término de búsqueda (dejar vacío para no filtrar): ")
                search_term = search_term_input if search_term_input else None
                
                # Mostrar categorías disponibles
                print("\nCategorías disponibles:")
                categories = self._category_repo.get_all()
                for cat in categories:
                    print(f"  - {cat.id}: {cat.name}")
                category_id_input = input("ID de Categoría (dejar vacío para no filtrar): ")
                category_id = category_id_input if category_id_input else None
                page = 1 # Reiniciar a la primera página con nuevos filtros
            elif action == 'r':
                search_term = None
                category_id = None
                page = 1
                print("Filtros reiniciados.")
            elif action == 'b':
                break
            else:
                print("Acción no reconocida.")

    def _view_product_details(self):
        """Muestra los detalles de un producto específico."""
        product_id = input("Ingrese el ID del producto para ver detalles: ")
        try:
            product_dto = self._get_product_details_use_case.execute(product_id)
            print("\n--- Detalles del Producto ---")
            print(f"ID: {product_dto.id}")
            print(f"Nombre: {product_dto.name}")
            print(f"Descripción: {product_dto.description}")
            print(f"Precio: ${product_dto.price:.2f}")
            print(f"Categoría: {product_dto.category_name}")
            print(f"Stock: {product_dto.stock}")
            print(f"Disponible: {'Sí' if product_dto.is_available else 'No'}")
        except ProductNotFoundException as e:
            print(f"Error: {e}")
        except DomainException as e:
            print(f"Error de dominio: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")
        input("Presione Enter para continuar...")

    def _craft_item(self):
        """Permite al usuario craftear un ítem."""
        print("\n--- Craftear Ítem ---")
        
        # Mostrar recetas disponibles
        recipes = self._recipe_repo.get_all()
        if not recipes:
            print("No hay recetas disponibles para craftear.")
            input("Presione Enter para continuar...")
            return

        print("\nRecetas disponibles:")
        for r in recipes:
            output_product = self._product_repo.get_by_id(r.output_product_id)
            output_name = output_product.name if output_product else "Producto Desconocido"
            print(f"  ID: {r.id:<10} | Nombre: {r.name:<30} | Crea: {r.output_quantity}x {output_name}")
            print("    Ingredientes:")
            for ing in r.ingredients:
                ing_product = self._product_repo.get_by_id(ing.product_id)
                ing_name = ing_product.name if ing_product else "Ingrediente Desconocido"
                print(f"      - {ing.quantity}x {ing_name}")
        
        recipe_id = input("\nIngrese el ID de la receta a craftear: ")
        try:
            quantity_str = input("Cantidad a craftear (por defecto 1): ")
            quantity = int(quantity_str) if quantity_str else 1
            
            request = CraftItemRequest(recipe_id=recipe_id, quantity=quantity)
            response = self._craft_item_use_case.execute(request)

            if response.success:
                print(f"Éxito: {response.message}")
            else:
                print(f"Fallo: {response.message}")

        except ValueError:
            print("Error: La cantidad debe ser un número entero.")
        except DomainException as e:
            print(f"Error de crafteo: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")
        input("Presione Enter para continuar...")

    def _show_inventory(self):
        """Muestra el inventario actual del usuario."""
        print("\n--- Inventario Actual ---")
        inventory_items = self._inventory_repo.get_all_inventory_items()
        
        if not inventory_items:
            print("El inventario está vacío.")
            input("Presione Enter para continuar...")
            return
        
        print("-" * 50)
        print(f"{'Producto':<30} | {'Cantidad':<10}")
        print("-" * 50)
        
        for product_id, item in inventory_items.items():
            product = self._product_repo.get_by_id(product_id)
            product_name = product.name if product else f"Producto Desconocido ({product_id})"
            print(f"{product_name:<30} | {item.quantity:<10}")
        print("-" * 50)
        input("Presione Enter para continuar...")

    def _add_stock_to_inventory(self):
        """Permite añadir stock a un producto existente en el inventario."""
        print("\n--- Añadir Stock al Inventario ---")
        product_id = input("Ingrese el ID del producto al que desea añadir stock: ")
        try:
            quantity_str = input("Ingrese la cantidad a añadir (entero positivo): ")
            quantity = int(quantity_str)
            if quantity <= 0:
                raise ValueError("La cantidad a añadir debe ser un número positivo.")
            
            self._update_inventory_use_case.execute(product_id, quantity)
            print(f"Se añadieron {quantity} unidades al producto '{product_id}'.")
        except ValueError as e:
            print(f"Error de entrada: {e}")
        except ProductNotFoundException as e:
            print(f"Error: {e}. Asegúrese de que el producto exista.")
        except DomainException as e:
            print(f"Error de dominio: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")
        input("Presione Enter para continuar...")


# Punto de entrada de la aplicación CLI
if __name__ == "__main__":
    app = CLIApp()
    app.run()

