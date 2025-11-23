from Application.Interfaces.recipe_repository import IRecipeRepository
from Application.Interfaces.inventory_repository import IInventoryRepository
from Application.Interfaces.product_repository import IProductRepository
from Application.DTOs.crafting_dtos import CraftItemRequest, CraftItemResponse
from Domain.Exceptions.custom_exceptions import (
    RecipeNotFoundException,
    InsufficientStockException,
    ProductNotFoundException,
    CraftingFailedException
)

class CraftItemUseCase:
    """Caso de Uso: Craftear un Ítem a partir de una Receta."""

    def __init__(self, recipe_repo: IRecipeRepository, inventory_repo: IInventoryRepository, product_repo: IProductRepository):
        self._recipe_repo = recipe_repo
        self._inventory_repo = inventory_repo
        self._product_repo = product_repo

    def execute(self, request: CraftItemRequest) -> CraftItemResponse:
        """
        Intenta craftear un ítem dada una receta y cantidad.
        Consume ingredientes y añade el producto resultante al inventario.
        """
        recipe = self._recipe_repo.get_by_id(request.recipe_id)
        if not recipe:
            raise RecipeNotFoundException(request.recipe_id)

        output_product = self._product_repo.get_by_id(recipe.output_product_id)
        if not output_product:
            raise ProductNotFoundException(recipe.output_product_id)

        try:
            # Verificar stock de ingredientes
            for ingredient in recipe.ingredients:
                required_quantity = ingredient.quantity * request.quantity
                available_quantity = self._inventory_repo.get_item_quantity(ingredient.product_id)
                if available_quantity < required_quantity:
                    raise InsufficientStockException(
                        product_id=ingredient.product_id,
                        requested=required_quantity,
                        available=available_quantity
                    )

            # Consumir ingredientes del inventario
            for ingredient in recipe.ingredients:
                self._inventory_repo.remove_item_quantity(ingredient.product_id, ingredient.quantity * request.quantity)

            # Añadir producto crafteado al inventario
            crafted_total_quantity = recipe.output_quantity * request.quantity
            self._inventory_repo.add_item_quantity(output_product.id, crafted_total_quantity)

            # Actualizar stock del producto (ej. para el catálogo)
            output_product.increase_stock(crafted_total_quantity)
            self._product_repo.update_product_stock(output_product.id, output_product.stock)


            return CraftItemResponse(
                crafted_product_id=output_product.id,
                crafted_quantity=crafted_total_quantity,
                success=True,
                message=f"Se craftearon {crafted_total_quantity} unidades de '{output_product.name}'."
            )

        except (InsufficientStockException, ProductNotFoundException) as e:
            return CraftItemResponse(
                crafted_product_id=recipe.output_product_id,
                crafted_quantity=0,
                success=False,
                message=str(e)
            )
        except Exception as e:
            raise CraftingFailedException(f"Error inesperado al craftear: {e}") from e

