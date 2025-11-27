from .models import Product


class ProductService:

    def get_all_products(self, category_id=None, search_term=None):
        products = Product.objects.all()

        if category_id:
            products = products.filter(category_id=category_id)

        if search_term:
            products = products.filter(
                name__icontains=search_term
            ) | products.filter(
                description__icontains=search_term
            )

        return products.order_by('name')

    def get_product_by_id(self, product_id):
        return Product.objects.get(id=product_id)

    def get_stock_info(self, product_id):
        product = Product.objects.get(id=product_id)
        return {
            "stock": product.stock,
            "availability_message": product.availability_message
        }


product_service = ProductService()
