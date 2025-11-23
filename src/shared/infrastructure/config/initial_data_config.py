from typing import List, Dict, Any

from Domain.Entities.product import Product
from Domain.Entities.category import Category
from Domain.Entities.inventory import InventoryItem
from Domain.Entities.recipe import Recipe, RecipeIngredient

class InitialDataConfig:
    """
    Clase de configuración para datos iniciales, emulando el patrón ScriptableObject.
    Contiene los datos "base" que se cargarán si no hay datos persistidos.
    """
    def __init__(self):
        self._categories_data: List[Dict[str, Any]] = [
            {"id": "cat-1", "name": "Herramientas"},
            {"id": "cat-2", "name": "Materiales"},
            {"id": "cat-3", "name": "Consumibles"},
            {"id": "cat-4", "name": "Armas"},
            {"id": "cat-5", "name": "Ropa"}
        ]

        self._products_data: List[Dict[str, Any]] = [
            {"id": "prod-1", "name": "Hacha de Piedra", "description": "Un hacha básica para cortar madera.", "price": 15.0, "category_id": "cat-1", "stock": 5},
            {"id": "prod-2", "name": "Pico de Piedra", "description": "Un pico básico para minar roca.", "price": 12.0, "category_id": "cat-1", "stock": 3},
            {"id": "prod-3", "name": "Madera", "description": "Troncos de madera cortados.", "price": 2.0, "category_id": "cat-2", "stock": 50},
            {"id": "prod-4", "name": "Piedra", "description": "Fragmentos de roca sin procesar.", "price": 1.0, "category_id": "cat-2", "stock": 100},
            {"id": "prod-5", "name": "Carne Cocinada", "description": "Carne asada, restaura algo de energía.", "price": 5.0, "category_id": "cat-3", "stock": 10},
            {"id": "prod-6", "name": "Arco Simple", "description": "Un arco rudimentario para la caza.", "price": 25.0, "category_id": "cat-4", "stock": 2},
            {"id": "prod-7", "name": "Flechas de Piedra", "description": "Flechas con puntas de piedra.", "price": 0.5, "category_id": "cat-4", "stock": 30},
            {"id": "prod-8", "name": "Saco de Cuero", "description": "Un simple saco de cuero para llevar ítems.", "price": 10.0, "category_id": "cat-5", "stock": 1},
            {"id": "prod-9", "name": "Carne Cruda", "description": "Carne fresca, se puede cocinar.", "price": 3.0, "category_id": "cat-3", "stock": 20},
            {"id": "prod-10", "name": "Piel Animal", "description": "Piel sin curtir de animales.", "price": 4.0, "category_id": "cat-2", "stock": 15},
            {"id": "prod-11", "name": "Cuerda", "description": "Cuerda hecha de fibras.", "price": 1.5, "category_id": "cat-2", "stock": 25},
            {"id": "prod-12", "name": "Antorcha", "description": "Proporciona luz en la oscuridad.", "price": 3.0, "category_id": "cat-1", "stock": 8},
            {"id": "prod-13", "name": "Mineral de Hierro", "description": "Mineral bruto de hierro.", "price": 6.0, "category_id": "cat-2", "stock": 0}, # Ejemplo sin stock inicial
            {"id": "prod-14", "name": "Lingote de Hierro", "description": "Barra de hierro fundido.", "price": 10.0, "category_id": "cat-2", "stock": 0},
            {"id": "prod-15", "name": "Espada de Hierro", "description": "Una espada robusta de hierro.", "price": 50.0, "category_id": "cat-4", "stock": 0},
            {"id": "prod-16", "name": "Botas de Cuero", "description": "Botas simples de cuero.", "price": 20.0, "category_id": "cat-5", "stock": 0},
            {"id": "prod-17", "name": "Planta Medicinal", "description": "Planta con propiedades curativas.", "price": 7.0, "category_id": "cat-3", "stock": 0},
            {"id": "prod-18", "name": "Poción de Salud Menor", "description": "Restaura una pequeña cantidad de salud.", "price": 10.0, "category_id": "cat-3", "stock": 0}
        ]
        
        # El inventario inicial puede ser diferente al stock general de productos
        self._initial_inventory_data: List[Dict[str, Any]] = [
            {"product_id": "prod-3", "quantity": 10}, # 10 unidades de Madera en inventario
            {"product_id": "prod-4", "quantity": 15}, # 15 unidades de Piedra en inventario
            {"id": "prod-9", "quantity": 5}, # Carne Cruda
            {"id": "prod-10", "quantity": 3}, # Piel Animal
            {"id": "prod-11", "quantity": 5}, # Cuerda
            {"id": "prod-12", "quantity": 2}, # Antorcha
        ]

        self._recipes_data: List[Dict[str, Any]] = [
            {
                "id": "recipe-1",
                "name": "Craftear Hacha de Piedra",
                "output_product_id": "prod-1",
                "output_quantity": 1,
                "ingredients": [
                    {"product_id": "prod-3", "quantity": 5},  # 5 Madera
                    {"product_id": "prod-4", "quantity": 3}   # 3 Piedra
                ]
            },
            {
                "id": "recipe-2",
                "name": "Craftear Pico de Piedra",
                "output_product_id": "prod-2",
                "output_quantity": 1,
                "ingredients": [
                    {"product_id": "prod-3", "quantity": 4},  # 4 Madera
                    {"product_id": "prod-4", "quantity": 4}   # 4 Piedra
                ]
            },
            {
                "id": "recipe-3",
                "name": "Craftear Flechas de Piedra",
                "output_product_id": "prod-7",
                "output_quantity": 5, # Craftea 5 flechas a la vez
                "ingredients": [
                    {"product_id": "prod-3", "quantity": 1},  # 1 Madera
                    {"product_id": "prod-4", "quantity": 1}   # 1 Piedra
                ]
            },
            {
                "id": "recipe-4",
                "name": "Cocinar Carne",
                "output_product_id": "prod-5",
                "output_quantity": 1,
                "ingredients": [
                    {"product_id": "prod-9", "quantity": 1}  # 1 Carne Cruda
                ]
            },
            {
                "id": "recipe-5",
                "name": "Hacer Saco de Cuero",
                "output_product_id": "prod-8",
                "output_quantity": 1,
                "ingredients": [
                    {"product_id": "prod-10", "quantity": 2}, # 2 Piel Animal
                    {"product_id": "prod-11", "quantity": 1} # 1 Cuerda
                ]
            },
            {
                "id": "recipe-6",
                "name": "Craftear Botas de Cuero",
                "output_product_id": "prod-16",
                "output_quantity": 1,
                "ingredients": [
                    {"product_id": "prod-10", "quantity": 3}, # 3 Piel Animal
                    {"product_id": "prod-11", "quantity": 2}  # 2 Cuerda
                ]
            },
            {
                "id": "recipe-7",
                "name": "Craftear Poción de Salud Menor",
                "output_product_id": "prod-18",
                "output_quantity": 1,
                "ingredients": [
                    {"product_id": "prod-17", "quantity": 2}, # 2 Planta Medicinal
                    {"product_id": "prod-1", "quantity": 1} # Ingrediente absurdo para demostrar flexibilidad.
                ]
            },
        ]

    def category_from_dict(self, data: Dict[str, Any]) -> Category:
        """Crea una entidad Category desde un diccionario."""
        return Category(**data)

    def product_from_dict(self, data: Dict[str, Any]) -> Product:
        """Crea una entidad Product desde un diccionario."""
        return Product(**data)

    def inventory_item_from_dict(self, data: Dict[str, Any]) -> InventoryItem:
        """Crea una entidad InventoryItem desde un diccionario."""
        return InventoryItem(**data)

    def recipe_ingredient_from_dict(self, data: Dict[str, Any]) -> RecipeIngredient:
        """Crea una entidad RecipeIngredient desde un diccionario."""
        return RecipeIngredient(**data)

    def recipe_from_dict(self, data: Dict[str, Any]) -> Recipe:
        """Crea una entidad Recipe desde un diccionario."""
        ingredients = [self.recipe_ingredient_from_dict(ing) for ing in data.pop("ingredients", [])]
        return Recipe(ingredients=ingredients, **data)

    def get_initial_categories(self) -> List[Category]:
        """Obtiene la lista inicial de entidades Category."""
        return [self.category_from_dict(data) for data in self._categories_data]

    def get_initial_products(self) -> List[Product]:
        """Obtiene la lista inicial de entidades Product."""
        return [self.product_from_dict(data) for data in self._products_data]

    def get_initial_inventory(self) -> List[InventoryItem]:
        """Obtiene la lista inicial de entidades InventoryItem."""
        return [self.inventory_item_from_dict(data) for data in self._initial_inventory_data]

    def get_initial_recipes(self) -> List[Recipe]:
        """Obtiene la lista inicial de entidades Recipe."""
        return [self.recipe_from_dict(data) for data in self._recipes_data]

